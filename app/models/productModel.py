from app.extensions import db
from app.models.baseModel import BaseModel

class Product(BaseModel, db.Model):
    """
    Model class representing a product entity.

    Inherits from BaseModel and db.Model.
    """

    __tablename__ = "products"

    # Columns for primary product information
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(256), nullable=True)

    # Define foreign keys linking to other tables
    seller_id = db.Column(db.String(256), db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.String(256), db.ForeignKey("categories.id"), nullable=False)
    business_id = db.Column(db.String(256), db.ForeignKey("business.id"), nullable=True)

    # Define relationships with other models
    seller = db.relationship("User", backref=db.backref("products", lazy=True))
    category = db.relationship("Category", backref=db.backref("products", lazy=True))
    business = db.relationship("Business", backref=db.backref("products", lazy=True))
