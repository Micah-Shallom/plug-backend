from app.extensions import db
from app.models.baseModel import BaseModel

class Category(BaseModel, db.Model):
    """
    Model class representing a category entity.

    Inherits from BaseModel and db.Model.
    """

    __tablename__ = "categories"

    # Column for category name
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Column for category description
    description = db.Column(db.String(500), unique=False, nullable=False)
