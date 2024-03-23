from flask import request, jsonify
from app.extensions import db
from app.contactInfo import payment_bp
from app.models.paymentInfoModel import PaymentInfo


# Create a new payment information entry
@payment_bp.route('/create', methods=['POST'])
def create_payment_info():
    data = request.get_json()
    new_payment_info = PaymentInfo(**data)

    try:
        new_payment_info.save(commit=True)
        return jsonify({"message": "Payment information created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get all payment information entries
@payment_bp.route('/all', methods=['GET'])
def get_all_payment_info():
    try:
        payment_info_list = PaymentInfo.query.all()
        result = []

        if not payment_info_list:
            return jsonify({"message": "empty payment information returned"}), 404
        
        for payment_info in payment_info_list:
            payment_info_data = {
                'bank_name': payment_info.bank_name,
                'account_number': payment_info.account_number,
                'account_holder_name': payment_info.account_holder_name,
                'address': payment_info.address,
                'city': payment_info.city,
                'state': payment_info.state
                # Add more fields as needed
            }
            result.append(payment_info_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Get a specific payment information entry by ID
@payment_bp.route('/<string:user_id>', methods=['GET'])
def get_payment_info(user_id):
    try:
        payment_info = PaymentInfo.query.filter_by(owner_id=user_id).first()

        if payment_info:
            payment_info_data = {
                'bank_name': payment_info.bank_name,
                'account_number': payment_info.account_number,
                'account_holder_name': payment_info.account_holder_name,
                'address': payment_info.address,
                'city': payment_info.city,
                'state': payment_info.state
                # Add more fields as needed
            }
            return jsonify(payment_info_data), 200
        else:
            return jsonify({"message": "payment information not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update a specific payment information entry by ID
@payment_bp.route('/update/<string:user_id>', methods=['PUT'])
def update_payment_info(user_id):
    try: 
        payment_info = PaymentInfo.query.filter_by(owner_id=user_id).first()
        data = request.get_json()

        if not payment_info:
            return jsonify({"message": "payment information not found"}), 404

        for key, value in data.items():
            setattr(payment_info, key, value)
        
        payment_info.save(commit=True)

        return jsonify({"message": "payment information updated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a specific payment information entry by ID
@payment_bp.route('/delete/<string:user_id>', methods=['DELETE'])
def delete_payment_info(user_id):
    payment_info = PaymentInfo.query.filter_by(owner_id=user_id).first_or_404()

    try:
        payment_info.delete(commit=True)
        return jsonify({"message": "payment information deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
