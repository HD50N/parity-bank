"""
REST API Router for Transaction Service
Implements OpenAPI 3 contract for transaction history retrieval
"""
from flask import Blueprint, request, jsonify
from data.mock_data import TRANSACTIONS
from .schemas import TransactionHistoryResponse, Error

rest_bp = Blueprint("transaction_rest", __name__)

@rest_bp.route("/accounts/<account_id>/transactions", methods=["GET"])
def get_transaction_history(account_id: str):
    """Get transaction history for an account"""
    
    # Get query parameters
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    
    # Validate account exists
    if account_id not in TRANSACTIONS:
        return jsonify({
            "code": "ACCOUNT_NOT_FOUND",
            "message": f"Account {account_id} not found"
        }), 404
    
    txns = TRANSACTIONS[account_id]
    
    # Apply date filters if provided
    if from_date or to_date:
        filtered = []
        for t in txns:
            d = t["date"][:10]  # Extract YYYY-MM-DD part
            if from_date and d < from_date:
                continue
            if to_date and d > to_date:
                continue
            filtered.append(t)
        txns = filtered
    
    # Build response
    response = {
        "account_id": account_id,
        "from_date": from_date or "",
        "to_date": to_date or "",
        "transaction_count": len(txns),
        "transactions": txns
    }
    
    return jsonify(response), 200

@rest_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        "code": "BAD_REQUEST",
        "message": "Invalid request parameters"
    }), 400

@rest_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "code": "NOT_FOUND", 
        "message": "Resource not found"
    }), 404
