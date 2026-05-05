from flask import Flask, send_from_directory
from services.account_service import account_bp
from services.transaction_service import transaction_bp
from services.transfer_service import transfer_bp
from services.customer_service import customer_bp

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")
app.register_blueprint(account_bp, url_prefix="/account")
app.register_blueprint(transaction_bp, url_prefix="/transaction")
app.register_blueprint(transfer_bp, url_prefix="/transfer")
app.register_blueprint(customer_bp, url_prefix="/customer")

if __name__ == "__main__":
    print("Parity Bank SOAP API — http://localhost:8000")
    print("  GetAccountBalance:     GET  http://localhost:8000/account?wsdl")
    print("  GetTransactionHistory: GET  http://localhost:8000/transaction?wsdl")
    print("  TransferFunds:         GET  http://localhost:8000/transfer?wsdl")
    print("  GetCustomerInfo:       GET  http://localhost:8000/customer?wsdl")
    app.run(host="0.0.0.0", port=8000, debug=False)
