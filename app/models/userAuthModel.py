from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.baseModel import BaseModel

class User(BaseModel, db.Model):
    """
    Model class representing a user entity.

    Inherits from BaseModel and db.Model.
    """

    __tablename__ = "users"

    # Columns for user information
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    role =  db.Column(db.String(60), nullable=True)
    fullname = db.Column(db.String(120), nullable=True)
    profile_picture =  db.Column(db.String(256))
    bio = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    secondary_email = db.Column(db.String(120), nullable=True)

    def __init__(self, fullname, username, email, password, role):
        """
        Initialize a user object with provided attributes.

        Args:
            fullname (str): Full name of the user.
            username (str): Unique username of the user.
            email (str): Unique email address of the user.
            password (str): Password of the user.
            role (str): Role of the user.
        """
        self.username = username
        self.fullname = fullname
        self.email = email
        self.role = role
        self.password = password
        self.set_password(password)

    def set_password(self, password):
        """
        Hashes the provided password and sets it as the user's password.

        Args:
            password (str): Password to be hashed.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the user's hashed password.

        Args:
            password (str): Password to be checked.

        Returns:
            bool: True if password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        """
        Retrieves a user object based on the username.

        Args:
            username (str): Username of the user to retrieve.

        Returns:
            User: User object corresponding to the username.
        """
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        """
        Retrieves a user object based on the email address.

        Args:
            email (str): Email address of the user to retrieve.

        Returns:
            User: User object corresponding to the email address.
        """
        return cls.query.filter_by(email=email).first()


class TokenBlockList(BaseModel, db.Model):
    """
    Model class for storing blocked JWT tokens.

    Inherits from BaseModel and db.Model.
    """

    __tablename__ = "tokenblocklist"

    jti = db.Column(db.String(), nullable=False)
