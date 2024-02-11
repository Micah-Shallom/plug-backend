from flask import Blueprint


category_bp = Blueprint("category",__name__)
product_bp = Blueprint("products",__name__)

from app.listings import categoryRoute
from app.listings import productRoute