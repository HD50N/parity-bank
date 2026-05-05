ACCOUNTS = {
    "ACC-001234": {
        "account_id": "ACC-001234",
        "balance": "15234.50",
        "currency": "USD",
        "account_type": "CHECKING",
        "status": "ACTIVE",
        "owner_name": "John Smith",
        "customer_id": "CUST-0001",
    },
    "ACC-005678": {
        "account_id": "ACC-005678",
        "balance": "42100.00",
        "currency": "USD",
        "account_type": "SAVINGS",
        "status": "ACTIVE",
        "owner_name": "Jane Doe",
        "customer_id": "CUST-0002",
    },
    "ACC-009999": {
        "account_id": "ACC-009999",
        "balance": "3.27",
        "currency": "USD",
        "account_type": "CHECKING",
        "status": "ACTIVE",
        "owner_name": "Bob Johnson",
        "customer_id": "CUST-0003",
    },
    "ACC-007777": {
        "account_id": "ACC-007777",
        "balance": "0.00",
        "currency": "USD",
        "account_type": "CHECKING",
        "status": "FROZEN",
        "owner_name": "Alice Brown",
        "customer_id": "CUST-0004",
    },
}

CUSTOMERS = {
    "CUST-0001": {
        "customer_id": "CUST-0001",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@paritybank.com",
        "phone": "555-0101",
        "address": "123 Main St, Springfield, IL 62701",
        "primary_account_id": "ACC-001234",
    },
    "CUST-0002": {
        "customer_id": "CUST-0002",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@paritybank.com",
        "phone": "555-0102",
        "address": "456 Oak Ave, Springfield, IL 62702",
        "primary_account_id": "ACC-005678",
    },
    "CUST-0003": {
        "customer_id": "CUST-0003",
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.johnson@paritybank.com",
        "phone": "555-0103",
        "address": "789 Pine Rd, Springfield, IL 62703",
        "primary_account_id": "ACC-009999",
    },
    "CUST-0004": {
        "customer_id": "CUST-0004",
        "first_name": "Alice",
        "last_name": "Brown",
        "email": "alice.brown@paritybank.com",
        "phone": "555-0104",
        "address": "321 Elm St, Springfield, IL 62704",
        "primary_account_id": "ACC-007777",
    },
}

TRANSACTIONS = {
    "ACC-001234": [
        {
            "id": "TXN-99887",
            "amount": "-250.00",
            "date": "2024-01-14T15:22:00",
            "description": "PURCHASE AT MERCHANT",
            "type": "DEBIT",
            "balance_after": "15234.50",
        },
        {
            "id": "TXN-99886",
            "amount": "1000.00",
            "date": "2024-01-13T09:00:00",
            "description": "DIRECT DEPOSIT PAYROLL",
            "type": "CREDIT",
            "balance_after": "15484.50",
        },
        {
            "id": "TXN-99885",
            "amount": "-45.99",
            "date": "2024-01-12T18:30:00",
            "description": "UTILITY PAYMENT",
            "type": "DEBIT",
            "balance_after": "14484.50",
        },
    ],
    "ACC-005678": [
        {
            "id": "TXN-88001",
            "amount": "500.00",
            "date": "2024-01-10T10:00:00",
            "description": "TRANSFER FROM CHECKING",
            "type": "CREDIT",
            "balance_after": "42100.00",
        },
    ],
    "ACC-009999": [
        {
            "id": "TXN-77001",
            "amount": "-96.73",
            "date": "2024-01-09T12:00:00",
            "description": "GROCERY STORE",
            "type": "DEBIT",
            "balance_after": "3.27",
        },
    ],
    "ACC-007777": [],
}

transfer_counter = [1000]
