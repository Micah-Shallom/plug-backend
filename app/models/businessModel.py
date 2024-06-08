from app.extensions import db
from app.models.baseModel import BaseModel

class Business(BaseModel, db.Model):
    """
    Model class representing a business entity.

    Inherits from BaseModel and db.Model.
    """

    __tablename__ = "business"

    # Columns definition
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(256), nullable=True)

    # Foreign key linking to the 'id' column in 'users' table
    owner_id = db.Column(db.String(500), db.ForeignKey("users.id"), nullable=False)

    # Relationship definition: business belongs to a user (owner)
    owner = db.relationship("User", backref=db.backref("business", lazy=True))

