from app.extensions import db
from app.models import BaseModel

class ContactInfo(BaseModel, db.Model):
    __tablename__ = 'contacts'

    #Primary Contact Information
    twitter = db.Column(db.String(256), nullable=True)
    instagram = db.Column(db.String(256), nullable=True)
    facebook = db.Column(db.String(256), nullable=True)
    youtube = db.Column(db.String(256), nullable=True)
    website = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    #Define foreign keys
    id = db.Column(db.String(256), db.ForeignKey("users.id"), nullable=False)

    #Define relationships
    user = db.relationship("User", backref=db.backref("contacts", lazy=True))

    def __repr__(self):
        return f"<ContactInfo(name='{self.name}', email='{self.email}', phone='{self.phone}', address='{self.address}')>"
