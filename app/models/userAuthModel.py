from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.baseModel import BaseModel


class User(BaseModel, db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    role =  db.Column(db.String(60), nullable=False)
    fullname = db.Column(db.String(120), nullable=True)
    profile_picture =  db.Column(db.String(256))
    bio = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    secondary_email = db.Column(db.String(120), nullable=True)

    def __init__(self,fullname, username, email, password, role) -> None:
        self.username = username
        self.full_name = fullname
        self.email = email
        self.role = role
        self.password = password
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class TokenBlockList(db.Model):
    __tablename__="tokenblocklist"

    jti = db.Column(db.String(), nullable=False)

    