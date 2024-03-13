from app.extensions import db
from app.models import BaseModel

class PaymentInfo(BaseModel, db.Model):
    __tablename__ = 'payment'

    owner_id = db.Column(db.String(256), db.ForeignKey("users.id"), unique=True , nullable=False) #unique is true because a user should hae only one contact information stored at a time

    #Primary payment information
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    account_holder_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)

    #Define relationships
    user = db.relationship("User", backref=db.backref("payment", lazy=True))

    def __repr__(self):
        return f"<PaymentInfo(id={self.id}, user_id={self.owner_id}, bank_name='{self.bank_name}', account_number='{self.account_number}')>"



