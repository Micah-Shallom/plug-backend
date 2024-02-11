from flask_jwt_extended import jwt_required
from flask import jsonify, request
from app.listings import category_bp
from app.models.categoryModel import Category
from app.utils.generators import admin_required
from app.models.productModel import Product


@category_bp.post("/add")
@jwt_required()
@admin_required
def create_category():
    data = request.get_json()

    try:
        new_category = Category(
            name = data.get("name"),
            description = data.get("description")
        )

        new_category.save()

        return jsonify({
            "message":"Category created successfully"
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# get products by category
@category_bp.get("/<string:category_id>/products")
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()

    product_list = list()

    for product in products:
        product_list.append(
            {
                "title": product.title,
                "description": product.description,
                "price": product.price
            }
        )
    
    return jsonify({
        "message": "Category Products fetched successfully",
        "results": product_list
    }), 201