"""Seed script for mock accounts.

Creates 1-3 accounts per customer (~20 accounts total).
"""

import uuid
from decimal import Decimal

from database.seed.seed_customers import CUSTOMERS

# Map customer UUIDs to their accounts
ACCOUNTS = [
    # Aarav Sharma - 2 accounts
    {"id": uuid.UUID("b1000001-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[0]["id"], "account_number_masked": "XXXX-XXXX-4501", "account_type": "savings", "available_balance": Decimal("125340.50"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000001-0000-0000-0000-000000000002"), "customer_id": CUSTOMERS[0]["id"], "account_number_masked": "XXXX-XXXX-4502", "account_type": "current", "available_balance": Decimal("452100.00"), "currency": "INR", "status": "active"},
    # Priya Patel - 2 accounts
    {"id": uuid.UUID("b1000002-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[1]["id"], "account_number_masked": "XXXX-XXXX-7801", "account_type": "savings", "available_balance": Decimal("89750.25"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000002-0000-0000-0000-000000000002"), "customer_id": CUSTOMERS[1]["id"], "account_number_masked": "XXXX-XXXX-7802", "account_type": "fixed_deposit", "available_balance": Decimal("500000.00"), "currency": "INR", "status": "active"},
    # Rohan Gupta - 1 account
    {"id": uuid.UUID("b1000003-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[2]["id"], "account_number_masked": "XXXX-XXXX-3301", "account_type": "savings", "available_balance": Decimal("34200.75"), "currency": "INR", "status": "active"},
    # Sneha Reddy - 2 accounts
    {"id": uuid.UUID("b1000004-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[3]["id"], "account_number_masked": "XXXX-XXXX-9101", "account_type": "savings", "available_balance": Decimal("210500.00"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000004-0000-0000-0000-000000000002"), "customer_id": CUSTOMERS[3]["id"], "account_number_masked": "XXXX-XXXX-9102", "account_type": "current", "available_balance": Decimal("780000.00"), "currency": "INR", "status": "active"},
    # Vikram Malhotra - 3 accounts
    {"id": uuid.UUID("b1000005-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[4]["id"], "account_number_masked": "XXXX-XXXX-5501", "account_type": "savings", "available_balance": Decimal("567800.00"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000005-0000-0000-0000-000000000002"), "customer_id": CUSTOMERS[4]["id"], "account_number_masked": "XXXX-XXXX-5502", "account_type": "current", "available_balance": Decimal("1250000.00"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000005-0000-0000-0000-000000000003"), "customer_id": CUSTOMERS[4]["id"], "account_number_masked": "XXXX-XXXX-5503", "account_type": "fixed_deposit", "available_balance": Decimal("2000000.00"), "currency": "INR", "status": "active"},
    # Ananya Krishnan - 1 account
    {"id": uuid.UUID("b1000006-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[5]["id"], "account_number_masked": "XXXX-XXXX-8801", "account_type": "savings", "available_balance": Decimal("45600.30"), "currency": "INR", "status": "active"},
    # Karthik Nair - 2 accounts
    {"id": uuid.UUID("b1000007-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[6]["id"], "account_number_masked": "XXXX-XXXX-2201", "account_type": "savings", "available_balance": Decimal("178900.00"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000007-0000-0000-0000-000000000002"), "customer_id": CUSTOMERS[6]["id"], "account_number_masked": "XXXX-XXXX-2202", "account_type": "current", "available_balance": Decimal("340000.00"), "currency": "INR", "status": "dormant"},
    # Meera Joshi - 1 account
    {"id": uuid.UUID("b1000008-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[7]["id"], "account_number_masked": "XXXX-XXXX-6601", "account_type": "savings", "available_balance": Decimal("12500.00"), "currency": "INR", "status": "active"},
    # Arjun Desai - 2 accounts
    {"id": uuid.UUID("b1000009-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[8]["id"], "account_number_masked": "XXXX-XXXX-4401", "account_type": "savings", "available_balance": Decimal("298000.00"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000009-0000-0000-0000-000000000002"), "customer_id": CUSTOMERS[8]["id"], "account_number_masked": "XXXX-XXXX-4402", "account_type": "fixed_deposit", "available_balance": Decimal("750000.00"), "currency": "INR", "status": "active"},
    # Divya Iyer - 2 accounts
    {"id": uuid.UUID("b1000010-0000-0000-0000-000000000001"), "customer_id": CUSTOMERS[9]["id"], "account_number_masked": "XXXX-XXXX-1101", "account_type": "savings", "available_balance": Decimal("156700.80"), "currency": "INR", "status": "active"},
    {"id": uuid.UUID("b1000010-0000-0000-0000-000000000002"), "customer_id": CUSTOMERS[9]["id"], "account_number_masked": "XXXX-XXXX-1102", "account_type": "current", "available_balance": Decimal("890000.00"), "currency": "INR", "status": "frozen"},
]
