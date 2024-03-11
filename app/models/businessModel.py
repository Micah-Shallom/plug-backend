from app.extensions import db
from app.models.baseModel import BaseModel

class Business(BaseModel, db.Model):
    __tablename__ = "business"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    owner_id = db.Column(db.String(500), db.ForeignKey("users.id") ,nullable=False)

    #setup relationship between business and seller
    owner = db.relationship("User", backref=db.backref("business", lazy=True))

