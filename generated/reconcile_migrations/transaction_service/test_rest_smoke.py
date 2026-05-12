"""
Smoke tests for Transaction Service REST API
"""
import unittest
from unittest.mock import patch
from flask import Flask
from .rest_router import rest_bp

class TestTransactionRestAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(rest_bp)
        self.client = self.app.test_client()
    
    @patch('generated.reconcile_migrations.transaction_service.rest_router.TRANSACTIONS')
    def test_get_transaction_history_success(self, mock_transactions):
        mock_transactions.__contains__ = lambda self, key: key == 'ACC123'
        mock_transactions.__getitem__ = lambda self, key: [
            {
                "id": "TXN001",
                "amount": 100.0,
                "date": "2023-01-01T10:00:00Z",
                "description": "Test transaction",
                "type": "credit",
                "balance_after": 500.0
            }
        ]
        
        response = self.client.get('/accounts/ACC123/transactions')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['account_id'], 'ACC123')
        self.assertEqual(data['transaction_count'], 1)
        self.assertEqual(len(data['transactions']), 1)
    
    @patch('generated.reconcile_migrations.transaction_service.rest_router.TRANSACTIONS')
    def test_get_transaction_history_account_not_found(self, mock_transactions):
        mock_transactions.__contains__ = lambda self, key: False
        
        response = self.client.get('/accounts/INVALID/transactions')
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['code'], 'ACCOUNT_NOT_FOUND')
    
    @patch('generated.reconcile_migrations.transaction_service.rest_router.TRANSACTIONS')
    def test_get_transaction_history_with_date_filters(self, mock_transactions):
        mock_transactions.__contains__ = lambda self, key: key == 'ACC123'
        mock_transactions.__getitem__ = lambda self, key: [
            {
                "id": "TXN001",
                "amount": 100.0,
                "date": "2023-01-15T10:00:00Z",
                "description": "Test transaction",
                "type": "credit",
                "balance_after": 500.0
            }
        ]
        
        response = self.client.get('/accounts/ACC123/transactions?from_date=2023-01-01&to_date=2023-01-31')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['from_date'], '2023-01-01')
        self.assertEqual(data['to_date'], '2023-01-31')

if __name__ == '__main__':
    unittest.main()
