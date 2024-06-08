from app.listings import seller_bp  # Importing the blueprint instance
from app.models import Product  # Importing the Product model from app.models
from flask import jsonify  # Importing jsonify from Flask for JSON responses

@seller_bp.get("/<string:seller_id>/products")
def get_products_by_seller(seller_id):
    try:
        # Query all products associated with the seller_id
        products = Product.query.filter_by(seller_id=seller_id).all()

        # Initialize an empty list to store product data
        product_list = []

        # Iterate over the products and construct product_data dictionaries
        for product in products:
            product_data = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'category_id': product.category_id,
                'business_id': product.business_id
            }
            product_list.append(product_data)

        # Return the list of products as JSON response
        return jsonify(product_list)

    except Exception as e:
        # Handle any exceptions and return a 500 Internal Server Error response
        return jsonify({"message": str(e)}), 500
