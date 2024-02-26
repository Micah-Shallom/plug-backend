from app.extensions import db
from app.utils import generate_uuid
from app.models.baseModel import BaseModel

class Category(BaseModel,db.Model):
    __tablename__ = "categories"

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)

