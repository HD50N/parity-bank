# Parity Bank

A simulated legacy bank SOAP API server with a 2005-era web portal. Used to demo the LedgerShift migration pipeline — the agent scans this codebase, discovers the SOAP endpoints, and LedgerShift converts them to modern REST APIs.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install flask
```

## Start

```bash
.venv/bin/python server.py
```

Then open **http://localhost:8000**

## Stop

`Ctrl+C` in the terminal. If you've lost the terminal:

```bash
lsof -ti:8000 | xargs kill -9
```

## Demo accounts

| Account ID | Name | Type | Status |
|---|---|---|---|
| ACC-001234 | John Smith | CHECKING | ACTIVE |
| ACC-005678 | Jane Doe | SAVINGS | ACTIVE |
| ACC-009999 | Bob Johnson | CHECKING | ACTIVE |
| ACC-007777 | Alice Brown | CHECKING | FROZEN |

PIN: any value

## SOAP endpoints

| Service | URL | WSDL |
|---|---|---|
| GetAccountBalance | POST /account | GET /account?wsdl |
| GetTransactionHistory | POST /transaction | GET /transaction?wsdl |
| TransferFunds | POST /transfer | GET /transfer?wsdl |
| GetCustomerInfo | POST /customer | GET /customer?wsdl |

Example requests are in `examples/`.

## Structure

```
server.py               entry point
services/
  account_service.py    GetAccountBalance
  transaction_service.py  GetTransactionHistory
  transfer_service.py   TransferFunds
  customer_service.py   GetCustomerInfo
data/
  mock_data.py          hardcoded accounts, customers, transactions
frontend/
  index.html            bank portal UI
examples/
  *.xml                 sample SOAP request/response pairs
```
