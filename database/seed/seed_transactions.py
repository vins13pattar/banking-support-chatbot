"""Seed script for mock transactions.

Creates 100+ fictional transactions across accounts with varied types and statuses.
"""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from database.seed.seed_accounts import ACCOUNTS

now = datetime.now(timezone.utc)


def _dt(days_ago: int, hour: int = 10) -> datetime:
    """Helper to create a datetime N days ago."""
    return now - timedelta(days=days_ago, hours=now.hour - hour)


# fmt: off
TRANSACTIONS = [
    # ===== Aarav Sharma - Savings (XXXX-4501) =====
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7001", "transaction_type": "upi", "amount": Decimal("2500.00"), "merchant": "Swiggy", "description": "Food delivery", "status": "completed", "transaction_date": _dt(1)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7002", "transaction_type": "upi", "amount": Decimal("8500.00"), "merchant": "Amazon India", "description": "Electronics purchase", "status": "completed", "transaction_date": _dt(1, 14)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7003", "transaction_type": "neft", "amount": Decimal("25000.00"), "merchant": "Rent Payment", "description": "Monthly rent transfer", "status": "completed", "transaction_date": _dt(3)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7004", "transaction_type": "atm", "amount": Decimal("10000.00"), "merchant": "ATM Koramangala", "description": "Cash withdrawal", "status": "completed", "transaction_date": _dt(5)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7005", "transaction_type": "upi", "amount": Decimal("1200.00"), "merchant": "Uber India", "description": "Ride payment", "status": "completed", "transaction_date": _dt(6)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000006"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7006", "transaction_type": "pos", "amount": Decimal("4500.00"), "merchant": "Reliance Fresh", "description": "Grocery shopping", "status": "completed", "transaction_date": _dt(7)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000007"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7007", "transaction_type": "upi", "amount": Decimal("850.00"), "merchant": "Netflix India", "description": "Subscription renewal", "status": "completed", "transaction_date": _dt(10)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000008"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7008", "transaction_type": "atm", "amount": Decimal("5000.00"), "merchant": "ATM MG Road", "description": "Cash withdrawal", "status": "failed", "transaction_date": _dt(2)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000009"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7009", "transaction_type": "upi", "amount": Decimal("8500.00"), "merchant": "Unknown Merchant", "description": "Suspicious transaction", "status": "completed", "transaction_date": _dt(1, 16)},
    {"id": uuid.UUID("c0000001-0000-0000-0000-000000000010"), "account_id": ACCOUNTS[0]["id"], "transaction_reference": "TXN-7010", "transaction_type": "imps", "amount": Decimal("15000.00"), "merchant": "Self Transfer", "description": "Transfer to current account", "status": "completed", "transaction_date": _dt(4)},

    # ===== Aarav Sharma - Current (XXXX-4502) =====
    {"id": uuid.UUID("c0000002-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[1]["id"], "transaction_reference": "TXN-7011", "transaction_type": "neft", "amount": Decimal("150000.00"), "merchant": "Vendor Payment", "description": "Business payment", "status": "completed", "transaction_date": _dt(2)},
    {"id": uuid.UUID("c0000002-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[1]["id"], "transaction_reference": "TXN-7012", "transaction_type": "neft", "amount": Decimal("75000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},

    # ===== Priya Patel - Savings (XXXX-7801) =====
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7013", "transaction_type": "upi", "amount": Decimal("3200.00"), "merchant": "Myntra", "description": "Clothing purchase", "status": "completed", "transaction_date": _dt(2)},
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7014", "transaction_type": "upi", "amount": Decimal("500.00"), "merchant": "Zomato", "description": "Food delivery", "status": "completed", "transaction_date": _dt(3)},
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7015", "transaction_type": "pos", "amount": Decimal("12000.00"), "merchant": "DMart", "description": "Monthly groceries", "status": "completed", "transaction_date": _dt(5)},
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7016", "transaction_type": "upi", "amount": Decimal("1500.00"), "merchant": "BookMyShow", "description": "Movie tickets", "status": "completed", "transaction_date": _dt(7)},
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7017", "transaction_type": "upi", "amount": Decimal("6000.00"), "merchant": "Flipkart", "description": "Home appliance", "status": "pending", "transaction_date": _dt(1)},
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000006"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7018", "transaction_type": "neft", "amount": Decimal("50000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000007"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7019", "transaction_type": "upi", "amount": Decimal("3200.00"), "merchant": "Myntra", "description": "Duplicate charge - clothing", "status": "completed", "transaction_date": _dt(2, 14)},
    {"id": uuid.UUID("c0000003-0000-0000-0000-000000000008"), "account_id": ACCOUNTS[2]["id"], "transaction_reference": "TXN-7020", "transaction_type": "atm", "amount": Decimal("5000.00"), "merchant": "ATM Indiranagar", "description": "ATM withdrawal - debited but no cash", "status": "failed", "transaction_date": _dt(4)},

    # ===== Rohan Gupta - Savings (XXXX-3301) =====
    {"id": uuid.UUID("c0000004-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[4]["id"], "transaction_reference": "TXN-7021", "transaction_type": "upi", "amount": Decimal("450.00"), "merchant": "Spotify India", "description": "Music subscription", "status": "completed", "transaction_date": _dt(8)},
    {"id": uuid.UUID("c0000004-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[4]["id"], "transaction_reference": "TXN-7022", "transaction_type": "upi", "amount": Decimal("2800.00"), "merchant": "Swiggy", "description": "Multiple food orders", "status": "completed", "transaction_date": _dt(3)},
    {"id": uuid.UUID("c0000004-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[4]["id"], "transaction_reference": "TXN-7023", "transaction_type": "imps", "amount": Decimal("10000.00"), "merchant": "Friend Transfer", "description": "Loan repayment to friend", "status": "completed", "transaction_date": _dt(5)},
    {"id": uuid.UUID("c0000004-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[4]["id"], "transaction_reference": "TXN-7024", "transaction_type": "neft", "amount": Decimal("35000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000004-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[4]["id"], "transaction_reference": "TXN-7025", "transaction_type": "upi", "amount": Decimal("750.00"), "merchant": "PhonePe Merchant", "description": "Unknown charge", "status": "completed", "transaction_date": _dt(1)},

    # ===== Sneha Reddy - Savings (XXXX-9101) =====
    {"id": uuid.UUID("c0000005-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[5]["id"], "transaction_reference": "TXN-7026", "transaction_type": "upi", "amount": Decimal("15000.00"), "merchant": "Tanishq", "description": "Jewellery purchase", "status": "completed", "transaction_date": _dt(2)},
    {"id": uuid.UUID("c0000005-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[5]["id"], "transaction_reference": "TXN-7027", "transaction_type": "pos", "amount": Decimal("8900.00"), "merchant": "Lifestyle", "description": "Clothing", "status": "completed", "transaction_date": _dt(4)},
    {"id": uuid.UUID("c0000005-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[5]["id"], "transaction_reference": "TXN-7028", "transaction_type": "neft", "amount": Decimal("80000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000005-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[5]["id"], "transaction_reference": "TXN-7029", "transaction_type": "upi", "amount": Decimal("2200.00"), "merchant": "BigBasket", "description": "Grocery delivery", "status": "completed", "transaction_date": _dt(6)},
    {"id": uuid.UUID("c0000005-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[5]["id"], "transaction_reference": "TXN-7030", "transaction_type": "atm", "amount": Decimal("20000.00"), "merchant": "ATM Jubilee Hills", "description": "Cash withdrawal", "status": "completed", "transaction_date": _dt(9)},

    # ===== Sneha Reddy - Current (XXXX-9102) =====
    {"id": uuid.UUID("c0000006-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[6]["id"], "transaction_reference": "TXN-7031", "transaction_type": "neft", "amount": Decimal("200000.00"), "merchant": "Client Payment", "description": "Freelance project payment", "status": "completed", "transaction_date": _dt(10)},
    {"id": uuid.UUID("c0000006-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[6]["id"], "transaction_reference": "TXN-7032", "transaction_type": "neft", "amount": Decimal("45000.00"), "merchant": "Tax Payment", "description": "Advance tax Q2", "status": "completed", "transaction_date": _dt(20)},

    # ===== Vikram Malhotra - Savings (XXXX-5501) =====
    {"id": uuid.UUID("c0000007-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[7]["id"], "transaction_reference": "TXN-7033", "transaction_type": "upi", "amount": Decimal("5000.00"), "merchant": "MakeMyTrip", "description": "Hotel booking", "status": "completed", "transaction_date": _dt(3)},
    {"id": uuid.UUID("c0000007-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[7]["id"], "transaction_reference": "TXN-7034", "transaction_type": "upi", "amount": Decimal("18000.00"), "merchant": "IRCTC", "description": "Train tickets", "status": "completed", "transaction_date": _dt(5)},
    {"id": uuid.UUID("c0000007-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[7]["id"], "transaction_reference": "TXN-7035", "transaction_type": "pos", "amount": Decimal("35000.00"), "merchant": "Croma Electronics", "description": "Laptop accessory", "status": "completed", "transaction_date": _dt(7)},
    {"id": uuid.UUID("c0000007-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[7]["id"], "transaction_reference": "TXN-7036", "transaction_type": "upi", "amount": Decimal("1500.00"), "merchant": "Dunzo", "description": "Quick commerce delivery", "status": "reversed", "transaction_date": _dt(2)},
    {"id": uuid.UUID("c0000007-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[7]["id"], "transaction_reference": "TXN-7037", "transaction_type": "neft", "amount": Decimal("120000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000007-0000-0000-0000-000000000006"), "account_id": ACCOUNTS[7]["id"], "transaction_reference": "TXN-7038", "transaction_type": "upi", "amount": Decimal("7500.00"), "merchant": "Apollo Pharmacy", "description": "Medical expenses", "status": "completed", "transaction_date": _dt(8)},

    # ===== Vikram Malhotra - Current (XXXX-5502) =====
    {"id": uuid.UUID("c0000008-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[8]["id"], "transaction_reference": "TXN-7039", "transaction_type": "neft", "amount": Decimal("500000.00"), "merchant": "Business Partner", "description": "Business payment", "status": "completed", "transaction_date": _dt(8)},
    {"id": uuid.UUID("c0000008-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[8]["id"], "transaction_reference": "TXN-7040", "transaction_type": "neft", "amount": Decimal("350000.00"), "merchant": "Client Invoice", "description": "Invoice settlement", "status": "completed", "transaction_date": _dt(12)},

    # ===== Ananya Krishnan - Savings (XXXX-8801) =====
    {"id": uuid.UUID("c0000009-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[10]["id"], "transaction_reference": "TXN-7041", "transaction_type": "upi", "amount": Decimal("1800.00"), "merchant": "Cafe Coffee Day", "description": "Coffee and snacks", "status": "completed", "transaction_date": _dt(1)},
    {"id": uuid.UUID("c0000009-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[10]["id"], "transaction_reference": "TXN-7042", "transaction_type": "upi", "amount": Decimal("3500.00"), "merchant": "Nykaa", "description": "Beauty products", "status": "completed", "transaction_date": _dt(4)},
    {"id": uuid.UUID("c0000009-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[10]["id"], "transaction_reference": "TXN-7043", "transaction_type": "neft", "amount": Decimal("42000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000009-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[10]["id"], "transaction_reference": "TXN-7044", "transaction_type": "upi", "amount": Decimal("650.00"), "merchant": "Ola", "description": "Cab ride", "status": "failed", "transaction_date": _dt(2)},

    # ===== Karthik Nair - Savings (XXXX-2201) =====
    {"id": uuid.UUID("c0000010-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[11]["id"], "transaction_reference": "TXN-7045", "transaction_type": "upi", "amount": Decimal("12000.00"), "merchant": "Samsung Store", "description": "Phone accessories", "status": "completed", "transaction_date": _dt(3)},
    {"id": uuid.UUID("c0000010-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[11]["id"], "transaction_reference": "TXN-7046", "transaction_type": "pos", "amount": Decimal("6500.00"), "merchant": "Decathlon", "description": "Sports equipment", "status": "completed", "transaction_date": _dt(6)},
    {"id": uuid.UUID("c0000010-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[11]["id"], "transaction_reference": "TXN-7047", "transaction_type": "neft", "amount": Decimal("65000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000010-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[11]["id"], "transaction_reference": "TXN-7048", "transaction_type": "upi", "amount": Decimal("2200.00"), "merchant": "Swiggy", "description": "Food delivery", "status": "completed", "transaction_date": _dt(1)},
    {"id": uuid.UUID("c0000010-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[11]["id"], "transaction_reference": "TXN-7049", "transaction_type": "imps", "amount": Decimal("30000.00"), "merchant": "Self Transfer", "description": "Transfer to savings", "status": "completed", "transaction_date": _dt(10)},

    # ===== Meera Joshi - Savings (XXXX-6601) =====
    {"id": uuid.UUID("c0000011-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[13]["id"], "transaction_reference": "TXN-7050", "transaction_type": "upi", "amount": Decimal("1200.00"), "merchant": "Dominos", "description": "Pizza delivery", "status": "completed", "transaction_date": _dt(1)},
    {"id": uuid.UUID("c0000011-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[13]["id"], "transaction_reference": "TXN-7051", "transaction_type": "upi", "amount": Decimal("450.00"), "merchant": "Google Play", "description": "App purchase", "status": "completed", "transaction_date": _dt(5)},
    {"id": uuid.UUID("c0000011-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[13]["id"], "transaction_reference": "TXN-7052", "transaction_type": "neft", "amount": Decimal("28000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000011-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[13]["id"], "transaction_reference": "TXN-7053", "transaction_type": "upi", "amount": Decimal("5500.00"), "merchant": "Ajio", "description": "Clothing purchase", "status": "completed", "transaction_date": _dt(3)},

    # ===== Arjun Desai - Savings (XXXX-4401) =====
    {"id": uuid.UUID("c0000012-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[14]["id"], "transaction_reference": "TXN-7054", "transaction_type": "upi", "amount": Decimal("4200.00"), "merchant": "Amazon India", "description": "Book and electronics", "status": "completed", "transaction_date": _dt(2)},
    {"id": uuid.UUID("c0000012-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[14]["id"], "transaction_reference": "TXN-7055", "transaction_type": "pos", "amount": Decimal("28000.00"), "merchant": "Vijay Sales", "description": "Washing machine EMI", "status": "completed", "transaction_date": _dt(5)},
    {"id": uuid.UUID("c0000012-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[14]["id"], "transaction_reference": "TXN-7056", "transaction_type": "neft", "amount": Decimal("95000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000012-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[14]["id"], "transaction_reference": "TXN-7057", "transaction_type": "upi", "amount": Decimal("9800.00"), "merchant": "Unknown Online Store", "description": "Unrecognised purchase", "status": "completed", "transaction_date": _dt(1)},
    {"id": uuid.UUID("c0000012-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[14]["id"], "transaction_reference": "TXN-7058", "transaction_type": "atm", "amount": Decimal("10000.00"), "merchant": "ATM Andheri", "description": "Cash withdrawal", "status": "completed", "transaction_date": _dt(8)},
    {"id": uuid.UUID("c0000012-0000-0000-0000-000000000006"), "account_id": ACCOUNTS[14]["id"], "transaction_reference": "TXN-7059", "transaction_type": "upi", "amount": Decimal("1100.00"), "merchant": "Paytm Mall", "description": "Mobile recharge", "status": "completed", "transaction_date": _dt(12)},

    # ===== Divya Iyer - Savings (XXXX-1101) =====
    {"id": uuid.UUID("c0000013-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[16]["id"], "transaction_reference": "TXN-7060", "transaction_type": "upi", "amount": Decimal("7500.00"), "merchant": "Meesho", "description": "Ethnic wear", "status": "completed", "transaction_date": _dt(2)},
    {"id": uuid.UUID("c0000013-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[16]["id"], "transaction_reference": "TXN-7061", "transaction_type": "upi", "amount": Decimal("2100.00"), "merchant": "Zomato", "description": "Dining out", "status": "completed", "transaction_date": _dt(4)},
    {"id": uuid.UUID("c0000013-0000-0000-0000-000000000003"), "account_id": ACCOUNTS[16]["id"], "transaction_reference": "TXN-7062", "transaction_type": "neft", "amount": Decimal("55000.00"), "merchant": "Salary Credit", "description": "Monthly salary", "status": "completed", "transaction_date": _dt(15)},
    {"id": uuid.UUID("c0000013-0000-0000-0000-000000000004"), "account_id": ACCOUNTS[16]["id"], "transaction_reference": "TXN-7063", "transaction_type": "pos", "amount": Decimal("15000.00"), "merchant": "Shoppers Stop", "description": "Apparel shopping", "status": "completed", "transaction_date": _dt(7)},
    {"id": uuid.UUID("c0000013-0000-0000-0000-000000000005"), "account_id": ACCOUNTS[16]["id"], "transaction_reference": "TXN-7064", "transaction_type": "upi", "amount": Decimal("900.00"), "merchant": "Hotstar", "description": "Streaming subscription", "status": "completed", "transaction_date": _dt(10)},
    {"id": uuid.UUID("c0000013-0000-0000-0000-000000000006"), "account_id": ACCOUNTS[16]["id"], "transaction_reference": "TXN-7065", "transaction_type": "upi", "amount": Decimal("4500.00"), "merchant": "PharmEasy", "description": "Medicine order", "status": "completed", "transaction_date": _dt(6)},

    # ===== Divya Iyer - Current FROZEN (XXXX-1102) =====
    {"id": uuid.UUID("c0000014-0000-0000-0000-000000000001"), "account_id": ACCOUNTS[17]["id"], "transaction_reference": "TXN-7066", "transaction_type": "neft", "amount": Decimal("300000.00"), "merchant": "Business Client", "description": "Project payment", "status": "completed", "transaction_date": _dt(30)},
    {"id": uuid.UUID("c0000014-0000-0000-0000-000000000002"), "account_id": ACCOUNTS[17]["id"], "transaction_reference": "TXN-7067", "transaction_type": "neft", "amount": Decimal("150000.00"), "merchant": "Suspicious Transfer", "description": "Large outgoing transfer", "status": "completed", "transaction_date": _dt(25)},
]
# fmt: on
