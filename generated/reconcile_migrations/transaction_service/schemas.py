"""
Data schemas for Transaction Service REST API
Corresponds to OpenAPI 3 component schemas
"""
from typing import List, Optional

class TransactionItem:
    """Transaction item schema"""
    def __init__(self, id: str, amount: float, date: str, description: str, 
                 type: str, balance_after: float):
        self.id = id
        self.amount = amount
        self.date = date
        self.description = description
        self.type = type
        self.balance_after = balance_after

class TransactionHistoryResponse:
    """Transaction history response schema"""
    def __init__(self, account_id: str, from_date: str, to_date: str,
                 transaction_count: int, transactions: List[TransactionItem]):
        self.account_id = account_id
        self.from_date = from_date
        self.to_date = to_date
        self.transaction_count = transaction_count
        self.transactions = transactions

class Error:
    """Error response schema"""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
