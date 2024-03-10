from app.extensions import db
from app.models.baseModel import BaseModel

class Product(BaseModel, db.Model):
    __tablename__ = "products"

    #Primary product information
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)


    #Define foreign keys
    seller_id = db.Column(db.String(256), db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.String(256), db.ForeignKey("categories.id"), nullable=False)
    business_id = db.Column(db.String(256), db.ForeignKey("business.id"), nullable=True)  #business id will be nullable because not everone who creates a product is a business owner


    #Define relationships
    seller = db.relationship("User", backref=db.backref("products", lazy=True))
    category = db.relationship("Category", backref=db.backref("products", lazy=True))
    business = db.relationship("Business", backref=db.backref("products", lazy=True))


    