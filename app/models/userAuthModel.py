from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

def generate_uuid():
    return str(uuid4())

class User(db.Model):
    __tablename__ = "users"

    uid = generate_uuid()

    id = db.Column(db.String(256), primary_key=True, default=uid)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    role =  db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password, role) -> None:
        self.username = username
        self.email = email
        self.role = role
        self.password = password
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()