from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models.productModel import Product
from app.listings import product_bp
from app.extensions import db

# create product
@product_bp.post("/create")
@jwt_required
def create_product():
    data =  request.get_json()

    seller_id = ""
    category_id = ""
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")

    if not(seller_id and category_id and title and price):
        return jsonify({
            "message":"Missing required fields"
        }), 400
    
    try:
        new_product = Product(
            seller_id,
            category_id,
            title,
            description,
            price
        )

        new_product.save()

        return jsonify({"message":"Listing created successfully"}), 200
    except Exception as e:
        return jsonify({"message":str(e)}), 500
    
# get all products
@product_bp.get("/all")
@jwt_required
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


# update product listing 
@product_bp.put("/update/<str:product_id>")
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"message":"Product not found"}), 404
    

    title = data.get("title")
    desctiption =  data.get("description")
    price = data.get("price")

    if not (title and desctiption and price):
        return jsonify({"message":"Missing required fields"}), 400
    
    product.title = title
    product.description = desctiption
    product.price = price

    try:
        db.session.commit()
        return jsonify({
            "message": "Product updated successfully"
        }), 201
    except Exception as e:
        return jsonify({"message", str(e)}), 500

# deete product listing
@product_bp.delete("/delete")
@jwt_required()
def delete_listing(listing_id):
    listing = Product.query.get(listing_id)
    if not listing:
        return jsonify({'message': 'Listing not found'}), 404

    try:
        db.session.delete(listing)
        db.session.commit()
        return jsonify({'message': 'Listing deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

