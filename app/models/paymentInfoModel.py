from app.extensions import db
from app.models import BaseModel

class PaymentInfo(BaseModel, db.Model):
    """
    Model class representing payment information for a user.

    Inherits from BaseModel and db.Model.
    """

    __tablename__ = 'payment'

    # Columns for primary payment information
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    account_holder_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)

    # Define foreign key linking to the 'id' column in 'users' table
    owner_id = db.Column(db.String(256), db.ForeignKey("users.id"), unique=True, nullable=False)

    # Define relationship: payment information belongs to a user
    user = db.relationship("User", backref=db.backref("payment", lazy=True))

    def __repr__(self):
        return f"<PaymentInfo(id={self.id}, user_id={self.owner_id}, bank_name='{self.bank_name}', account_number='{self.account_number}')>"
