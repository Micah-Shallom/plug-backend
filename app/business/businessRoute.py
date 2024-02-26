from flask import request
from app.business import business_bp


@business_bp.route("<string:seller_id>")
def create_business(seller_id):
    pass