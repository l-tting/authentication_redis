from flask import Flask 
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'DELETE']
csrf = CSRFProtect(app)






