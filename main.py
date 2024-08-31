from flask import Flask, render_template, request,flash,redirect,url_for,session
from flask_mail import Mail, Message
from flask_login import LoginManager,login_required,login_user
from flask_redis import FlaskRedis
from werkzeug.security import generate_password_hash,check_password_hash
from shared import app
from datetime import timedelta
from forms import ResetPasswordForm,LoginForm,RegisterForm,OTPForm,PasswordForm
from models import User,db
import random



login_manager  = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = 'sjdjdfkkkfk'

#redis
app.config['REDIS_URL'] ='redis://localhost:6379/0'
redis_client = FlaskRedis(app)

# Configurations (use environment variables for sensitive information)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS']= False
app.config['MAIL_USE_SSL']= True
app.config['MAIL_USERNAME'] = 'brianletting01@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'brianletting01@gmail.com'
app.config['MAIL_PASSWORD'] = 'grcn ylld hgfr zqxt'

mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_otp():
    return random.randint(100000,999999)

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/mypage')
def page():
    return render_template("mypage.html")

@app.route('/login',methods= ['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data 
        user = db.session.query(User).filter(User.email==email).first()
        if not user:
            flash("User does not exist","error")
        else:
            check_password = check_password_hash(user.password,form.password.data)
            if not check_password:
                flash("wrong password","error")
            else:
                login_user(user)
                flash('Login successful','success')
                return redirect(url_for('page'))
    return render_template("login.html",form=form)

@app.route('/register',methods= ['GET','POST'])
def register():
    form = RegisterForm()  # Define the form outside the if block
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("User already exists.Please Login",'error')
            else:
                hashed_password = generate_password_hash(form.password.data)
                new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
    return render_template("register.html",form=form)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetPasswordForm()
    if request.method == 'POST':
        email = form.email.data
        user = db.session.query(User).filter(User.email==email).first()
        if  not user:
            flash("User does not exist","error")
        else:
            otp = generate_otp()
            redis_key = f'otp:{user.id}'
            redis_client.setex(redis_key, timedelta(minutes=10), otp)
            redis_client.setex(f'{redis_key}_expiration', timedelta(minutes=10), 'valid')
            message = Message(f'From {email}', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
            message.body = f' Your otp code is {otp}'
            try: 
                mail.send(message)
                flash("OTP sent successfully","success")
                session['reset_user_id'] = user.id
                return redirect(url_for('verify_otp'))
            except Exception as e:
                flash(f"Error sending mail ,{e}","error")
    return render_template('reset.html',form=form)


@app.route('/otpverification',methods=['GET','POST'])
def verify_otp():
    form= OTPForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            otp = form.otp.data
            user_id = session.get('reset_user_id')
            print(f"user_id:{user_id}")
            redis_key = f'otp:{user_id}'
            stored_otp = redis_client.get(redis_key)   
            if stored_otp:
                if str(otp) == stored_otp.decode('utf-8'):
                    flash("OTP verified. You are now logged in.", "success")
                    redis_client.delete(redis_key)
                    redis_client.delete(f'{redis_key}_expiration')
                    return redirect(url_for('password_reset'))
                else:
                    flash("Invalid otp","error")
            else:
                flash("Invalid OTP or OTP has expired, request new OTP","error")           
    return render_template("otp.html",form=form)
 

@app.route('/passwordreset',methods=['GET','POST'])
def password_reset():
    form = PasswordForm()
    if request.method == 'POST':
         if form.validate_on_submit():
            password = form.password.data
            confirm_password = form.confirm_password.data
            if password == confirm_password:
                 hashed_password = generate_password_hash(password)
                 user_id = session.get('reset_user_id')
                 user = db.session.query(User).filter(User.id==user_id).first()
                 if user:
                    user.password = hashed_password
                    db.session.commit()
                    flash("Password changed successfully")
            else:
                flash("Passwords don't match","error")
    return render_template("resetpassword.html",form=form)

if __name__ == '__main__':
    app.run(debug=True)
