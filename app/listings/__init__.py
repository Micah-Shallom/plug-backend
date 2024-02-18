from flask import Blueprint


category_bp = Blueprint("categories",__name__)
product_bp = Blueprint("products",__name__)
seller_bp = Blueprint("sellers",__name__)
search_bp = Blueprint("search",__name__)

from app.listings import categoryRoute, productRoute, sellersRoute, searchRoute