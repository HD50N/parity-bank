"""
Legacy SOAP Service: TransactionService
This service has been migrated to REST.
SOAP endpoint disabled - use REST API at /accounts/{accountId}/transactions
"""
from flask import Blueprint, jsonify

transaction_bp = Blueprint("transaction", __name__)

# Legacy SOAP endpoint disabled - return 410 Gone
@transaction_bp.route("", methods=["GET", "POST"])
def handle():
    return jsonify({
        "code": "DEPRECATED",
        "message": "SOAP service deprecated. Use REST API: GET /accounts/{accountId}/transactions"
    }), 410

# Remove all SOAP-related code:
# - soap_envelope() function
# - soap_fault() function 
# - XML parsing and SOAP operation handling
# - WSDL definition
# Business logic moved to REST service at generated/reconcile_migrations/transaction_service/
