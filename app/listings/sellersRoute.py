from app.listings import seller_bp
from app.models import Product
from flask import jsonify


@seller_bp.get("/<string:seller_id>/products")
def get_products_by_seller(seller_id):

    try:
        products = Product.query.filter_by(seller_id=seller_id).all()
        product_list = list()

        for product in products:
            product_list.append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'category_id': product.category_id,
                'business_id': product.business_id
            })

        return jsonify(product_list)

    except Exception as e:
        return jsonify({"message", str(e)}), 500
