from flask import Blueprint, jsonify, request
from data.mock_data import CUSTOMERS

customer_rest_bp = Blueprint("customer_rest", __name__)


@customer_rest_bp.route("/customers/<customer_id>", methods=["GET"])
def get_customer_info(customer_id):
    """Get customer information by ID"""
    if not customer_id:
        return jsonify({
            "code": "INVALID_INPUT",
            "message": "Customer ID is required"
        }), 400
    
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return jsonify({
            "code": "NOT_FOUND",
            "message": f"Customer not found: {customer_id}"
        }), 404
    
    return jsonify({
        "customer_id": customer["customer_id"],
        "first_name": customer["first_name"],
        "last_name": customer["last_name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "address": customer["address"],
        "primary_account_id": customer["primary_account_id"]
    }), 200
