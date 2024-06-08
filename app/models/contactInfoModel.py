from app.extensions import db
from app.models import BaseModel

class ContactInfo(BaseModel, db.Model):
    """
    Model class representing contact information for a user.

    Inherits from BaseModel and db.Model.
    """

    __tablename__ = 'contacts'

    # Primary Contact Information
    twitter = db.Column(db.String(256), nullable=True)
    instagram = db.Column(db.String(256), nullable=True)
    facebook = db.Column(db.String(256), nullable=True)
    youtube = db.Column(db.String(256), nullable=True)
    website = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    # Define foreign key linking to the 'id' column in 'users' table
    owner_id = db.Column(db.String(256), db.ForeignKey("users.id"), unique=True, nullable=False)

    # Define relationship: contact information belongs to a user
    user = db.relationship("User", backref=db.backref("contacts", lazy=True))
