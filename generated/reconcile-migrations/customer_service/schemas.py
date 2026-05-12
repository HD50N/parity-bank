from typing import Dict, Any


class CustomerSchema:
    """Customer response schema validation and serialization"""
    
    @staticmethod
    def validate_customer_data(customer_data: Dict[str, Any]) -> bool:
        """Validate customer data has required fields"""
        required_fields = [
            "customer_id", "first_name", "last_name", 
            "email", "phone", "address", "primary_account_id"
        ]
        return all(field in customer_data for field in required_fields)
    
    @staticmethod
    def serialize_customer(customer_data: Dict[str, Any]) -> Dict[str, str]:
        """Serialize customer data to REST response format"""
        return {
            "customer_id": str(customer_data["customer_id"]),
            "first_name": str(customer_data["first_name"]),
            "last_name": str(customer_data["last_name"]),
            "email": str(customer_data["email"]),
            "phone": str(customer_data["phone"]),
            "address": str(customer_data["address"]),
            "primary_account_id": str(customer_data["primary_account_id"])
        }


class ErrorSchema:
    """Error response schema"""
    
    @staticmethod
    def serialize_error(code: str, message: str) -> Dict[str, str]:
        """Serialize error response"""
        return {
            "code": code,
            "message": message
        }
