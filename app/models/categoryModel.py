from app.extensions import db
from app.utils import generate_uuid


class Category(db.Model):
    __tablename__ = "categories"

    uid = generate_uuid()

    category_id = db.Column(db.String(256), primary_key=True, default=uid)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"Category {self.name} created!"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
