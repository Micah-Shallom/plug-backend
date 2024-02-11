from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.models.productModel import Product
from app.models.categoryModel import Category
from app.listings import product_bp
from app.extensions import db
from app.utils.generators import is_seller

# create product
@product_bp.post("/create")
@jwt_required()
@is_seller
def create_product():
    data =  request.get_json()
    category = Category.query.filter_by(name=data.get("category")).first()

    seller_id = current_user.id
    category_id = category.category_id
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")

    if not(seller_id and category_id and title and price):
        return jsonify({
            "message":"Missing required fields"
        }), 400
    
    try:
        new_product = Product(
            seller_id = seller_id,
            category_id = category_id,
            title = title,
            description = description,
            price = price
        )

        new_product.save()

        return jsonify({"message":"Product Listing created successfully"}), 200
    except Exception as e:
        return jsonify({"message":str(e)}), 500
    
# get all products
@product_bp.get("/all")
def get_products():
    try:
        products = Product.query.all()
        product_list = list()

        for product in products:
            product_list.append({
                "id": product.product_id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
            })

        return jsonify(product_list)

    except Exception as e:
        return jsonify({"message", str(e)}), 500

# get product listing by id
@product_bp.get("/<string:product_id>")
def get_product_by_id(product_id):
    product = Product.query.get_or_404(product_id)

    data = dict()

    data["id"] = product.product_id
    data["title"] = product.title
    data["description"] = product.description
    data["price"] = product.price

    return jsonify({
        "message": "product fetched successfully",
        "result" : data
    })

# update product listing 
@product_bp.put("/update/<string:product_id>")
@jwt_required()
@is_seller
def update_product(product_id):
    data = request.get_json()
    product = Product.query.filter_by(product_id=product_id).first()

    print(product.title)
    # return jsonify({"":""}), 200

    if not product:
        return jsonify({"message":"Product not found"}), 404
    
    for key, val in data.items():
        if not product.key:
            return jsonify({"message":"Attempting to update field that does not exist"}), 400

        product[key] = val
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Product updated successfully",
            "result": product
        }), 201
    except Exception as e:
        return jsonify({"message", str(e)}), 500

# delete product listing
@product_bp.delete("/delete/<string:product_id>")
@is_seller
@jwt_required()
def delete_listing(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'product not found'}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
