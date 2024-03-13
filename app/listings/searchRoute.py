from flask import request, jsonify
from app.listings import search_bp
from app.models import Product


@search_bp.get("/")
def search_products():

    try:
        #get the  search query from the request parameters
        query = request.args.get("query")

        if not query:
            return jsonify({"error": "No search query provided"}), 400
        

        #Perform full text-search using postgresql full-text search capabilities
        #Titles and descriptions fields are indexed for full-text search
        results = Product.query.filter(
            Product.title.match(query) | Product.description.match(query)
        ).all()

        #Convert search results to json format
        search_results = []
        for product in results:
            product_data = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'category_id': product.category_id,
                'business_id': product.business_id
            }
            search_results.append(product_data)
        

        return jsonify({"search_results": search_results}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    