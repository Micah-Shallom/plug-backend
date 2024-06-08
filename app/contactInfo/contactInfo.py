from flask import request, jsonify
from app.extensions import db
from app.contactInfo import contact_bp
from app.models.contactInfoModel import ContactInfo

# Create a new contact information entry
@contact_bp.route('/create', methods=['POST'])
def create_contact_info():
    data = request.get_json()
    new_contact_info = ContactInfo(**data)

    try:
        new_contact_info.save(commit=True)
        return jsonify({"message": "Contact information created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get all contact information entries
@contact_bp.route('/all', methods=['GET'])
def get_all_contact_info():
    try:
        contact_info_list = ContactInfo.query.all()
        result = []

        if not contact_info_list:
            return jsonify({"message": "No contact information found"}), 404
        
        for contact_info in contact_info_list:
            contact_info_data = {
                'twitter': contact_info.twitter,
                'instagram': contact_info.instagram,
                'facebook': contact_info.facebook,
                'youtube': contact_info.youtube,
                'website': contact_info.website,
                'address': contact_info.address,
                'phone': contact_info.phone,
                # Add more fields as needed
            }
            result.append(contact_info_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a specific contact information entry by owner ID
@contact_bp.route('/<string:user_id>', methods=['GET'])
def get_contact_info(user_id):
    try:
        contact_info = ContactInfo.query.filter_by(owner_id=user_id).first()

        if contact_info:
            contact_info_data = {
                'twitter': contact_info.twitter,
                'instagram': contact_info.instagram,
                'facebook': contact_info.facebook,
                'youtube': contact_info.youtube,
                'website': contact_info.website,
                'address': contact_info.address,
                'phone': contact_info.phone
            }
            return jsonify(contact_info_data), 200
        else:
            return jsonify({"message": "Contact information not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update a specific contact information entry by owner ID
@contact_bp.route('/update/<string:user_id>', methods=['PUT'])
def update_contact_info(user_id):
    try: 
        contact_info = ContactInfo.query.filter_by(owner_id=user_id).first()
        data = request.get_json()

        if not contact_info:
            return jsonify({"message": "Contact information not found"}), 404

        # Update each field with the provided data
        for key, value in data.items():
            setattr(contact_info, key, value)
        
        contact_info.save(commit=True)

        return jsonify({"message": "Contact information updated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a specific contact information entry by owner ID
@contact_bp.route('/delete/<string:user_id>', methods=['DELETE'])
def delete_contact_info(user_id):
    contact_info = ContactInfo.query.filter_by(owner_id=user_id).first_or_404()

    try:
        contact_info.delete(commit=True)
        return jsonify({"message": "Contact information deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
