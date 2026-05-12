import unittest
import json
from flask import Flask
from rest_router import customer_rest_bp


class TestCustomerRestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(customer_rest_bp)
        self.client = self.app.test_client()
    
    def test_get_customer_info_success(self):
        """Test successful customer retrieval"""
        response = self.client.get('/customers/12345')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('customer_id', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertIn('email', data)
        self.assertIn('phone', data)
        self.assertIn('address', data)
        self.assertIn('primary_account_id', data)
    
    def test_get_customer_info_not_found(self):
        """Test customer not found scenario"""
        response = self.client.get('/customers/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['code'], 'NOT_FOUND')
        self.assertIn('Customer not found', data['message'])
    
    def test_get_customer_info_empty_id(self):
        """Test empty customer ID handling"""
        response = self.client.get('/customers/')
        # Flask routing will return 404 for missing path parameter
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
