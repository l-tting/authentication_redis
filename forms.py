from  flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[ DataRequired()],render_kw= {"placeholder":"Enter Name"})
    email = StringField("Email",validators=[ DataRequired(),Email()],render_kw= {"placeholder":"Enter Email"})
    password = PasswordField("Password",validators=[ DataRequired()],render_kw= {"placeholder":"Enter Password"})
    submit = SubmitField("Regsiter")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder":"Enter Email"})
    password = PasswordField("Password",validators=[DataRequired(),Email()],render_kw={"placeholder":"Enter Password"})
    submit = SubmitField("Login")

class ResetPasswordForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder":"Enter Email"})
    submit = SubmitField("Request Password Request")

class NewPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired(),Email()],render_kw={"placeholder":"New Password"})
    confrim_password = PasswordField("Password",validators=[DataRequired(),Email()],render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField("Change Password")

class OTPForm(FlaskForm):
    otp = IntegerField("OTP",validators=[DataRequired()],render_kw={"placeholder":"Enter OTP Code"})
    submit = SubmitField("Enter Code")

class PasswordForm(FlaskForm):
    password= StringField("password",validators=[DataRequired()],render_kw={"placeholder":"Enter New Password"})
    confirm_password= StringField("confirm_password",validators=[DataRequired()],render_kw={"placeholder":"Confirm New Password"})
    submit = SubmitField("Change Password")


