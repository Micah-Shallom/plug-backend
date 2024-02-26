from app.extensions import db
from app.models.baseModel import BaseModel

class BusinessModel(BaseModel, db.Model):
    __tablename__ = "business"

    name = db.Column(db.String(254), nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.String(500), db.ForeignKey("users.id") ,nullable=False)

    #setup relationship between business and seller
    owner = db.relationship("User", backref=db.backref("business", lazy=True))

