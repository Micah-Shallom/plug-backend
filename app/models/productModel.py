from app.extensions import db
from app.utils import generate_uuid


class Product(db.Model):
    __tablename__ = "products"

    uid = generate_uuid()
    product_id = db.Column(db.String(256), primary_key=True, default = uid)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.String(256), db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.String(256), db.ForeignKey("categories.category_id"), nullable=False)

    seller = db.relationship("User", backref=db.backref("products", lazy=True))
    category = db.relationship("Category", backref=db.backref("products", lazy=True))

    def __repr__(self):
        return '<Product %r>' % self.title
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    