"""Seed script for mock customers.

Creates 10 fictional Indian bank customers for demonstration.
"""

import uuid

CUSTOMERS = [
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567801"),
        "customer_number": "CUST-1001",
        "full_name": "Aarav Sharma",
        "email": "aarav.sharma@example.com",
        "phone_masked": "XXXX-XX-8901",
        "date_of_birth": "1990-05-15",
        "verification_answer": "8901",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567802"),
        "customer_number": "CUST-1002",
        "full_name": "Priya Patel",
        "email": "priya.patel@example.com",
        "phone_masked": "XXXX-XX-4523",
        "date_of_birth": "1988-11-22",
        "verification_answer": "4523",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567803"),
        "customer_number": "CUST-1003",
        "full_name": "Rohan Gupta",
        "email": "rohan.gupta@example.com",
        "phone_masked": "XXXX-XX-7712",
        "date_of_birth": "1995-03-08",
        "verification_answer": "7712",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567804"),
        "customer_number": "CUST-1004",
        "full_name": "Sneha Reddy",
        "email": "sneha.reddy@example.com",
        "phone_masked": "XXXX-XX-3345",
        "date_of_birth": "1992-07-30",
        "verification_answer": "3345",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567805"),
        "customer_number": "CUST-1005",
        "full_name": "Vikram Malhotra",
        "email": "vikram.malhotra@example.com",
        "phone_masked": "XXXX-XX-9988",
        "date_of_birth": "1985-12-01",
        "verification_answer": "9988",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567806"),
        "customer_number": "CUST-1006",
        "full_name": "Ananya Krishnan",
        "email": "ananya.krishnan@example.com",
        "phone_masked": "XXXX-XX-6621",
        "date_of_birth": "1993-09-14",
        "verification_answer": "6621",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567807"),
        "customer_number": "CUST-1007",
        "full_name": "Karthik Nair",
        "email": "karthik.nair@example.com",
        "phone_masked": "XXXX-XX-5540",
        "date_of_birth": "1991-01-25",
        "verification_answer": "5540",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567808"),
        "customer_number": "CUST-1008",
        "full_name": "Meera Joshi",
        "email": "meera.joshi@example.com",
        "phone_masked": "XXXX-XX-2289",
        "date_of_birth": "1997-06-18",
        "verification_answer": "2289",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567809"),
        "customer_number": "CUST-1009",
        "full_name": "Arjun Desai",
        "email": "arjun.desai@example.com",
        "phone_masked": "XXXX-XX-1177",
        "date_of_birth": "1989-04-03",
        "verification_answer": "1177",
    },
    {
        "id": uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567810"),
        "customer_number": "CUST-1010",
        "full_name": "Divya Iyer",
        "email": "divya.iyer@example.com",
        "phone_masked": "XXXX-XX-8834",
        "date_of_birth": "1994-10-27",
        "verification_answer": "8834",
    },
]
