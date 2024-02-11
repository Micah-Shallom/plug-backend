from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models.productModel import Product
from app.listings import product_bp
from app.extensions import db
from app.utils.generators import is_buyer, is_seller

# create product
@product_bp.post("/create")
@is_seller()
@jwt_required()
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
@product_bp.get("/<str:product_id>")
def get_product_by_id(product_id):
    product = Product.query.get_or_404(product_id)

    data = dict()

    data["id"] = product.product_id
    data["title"] = product.title
    data["description"] = product.description
    data["price"] = product.price

    return jsonify({
        "message": "prodct fetched successfully",
        "result" : data
    })

# update product listing 
@product_bp.put("/update/<str:product_id>")
@is_seller()
@jwt_required()
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
            "message": "Product updated successfully",
            "result": product
        }), 201
    except Exception as e:
        return jsonify({"message", str(e)}), 500

# delete product listing
@product_bp.delete("/delete/<str:product_id>")
@is_seller()
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
    
