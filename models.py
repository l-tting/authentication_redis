from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from shared import app
from flask_login import UserMixin


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6979@localhost/authh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200))
    email = db.Column(db.String,unique=True)
    password = db.Column(db.String)


with app.app_context():
    db.create_all()

