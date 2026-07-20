"""Seed script for banking knowledge base documents.

Creates 25+ FAQ and policy documents for the FAQ agent.
"""

import uuid

KNOWLEDGE_DOCUMENTS = [
    # ===== General Banking =====
    {
        "id": uuid.UUID("d0000001-0000-0000-0000-000000000001"),
        "title": "Bank Working Hours",
        "category": "general",
        "content": "Our bank branches are open Monday to Friday from 10:00 AM to 4:00 PM, and Saturday from 10:00 AM to 1:00 PM. Branches are closed on Sundays and gazetted holidays. ATM services are available 24 hours a day, 7 days a week. Internet banking and mobile banking services are available round the clock. Customer care helpline is available from 8:00 AM to 10:00 PM on all days.",
    },
    {
        "id": uuid.UUID("d0000001-0000-0000-0000-000000000002"),
        "title": "How to Update Address",
        "category": "general",
        "content": "To update your address, you can: (1) Visit your nearest branch with a valid address proof (Aadhaar, utility bill, passport). (2) Use internet banking: Navigate to Profile > Address Update > Submit new address with uploaded proof. (3) Through mobile app: Go to More > Profile Settings > Address. Address changes are verified within 2-3 working days. A confirmation SMS and email will be sent upon successful update.",
    },
    {
        "id": uuid.UUID("d0000001-0000-0000-0000-000000000003"),
        "title": "Documents Required to Open an Account",
        "category": "general",
        "content": "To open a new bank account, you need: (1) Identity proof: Aadhaar card, PAN card, or Passport. (2) Address proof: Aadhaar card, utility bill (within 3 months), or rental agreement. (3) Passport-size photographs: 2 recent photographs. (4) PAN card: Mandatory for all account types. (5) Initial deposit: ₹500 for savings account, ₹10,000 for current account. In-person KYC verification is required at the branch. Video KYC is available for select account types.",
    },
    {
        "id": uuid.UUID("d0000001-0000-0000-0000-000000000004"),
        "title": "Customer Grievance Redressal",
        "category": "general",
        "content": "If you have a complaint: (1) Contact our customer care at 1800-XXX-XXXX (toll-free). (2) Email: grievance@examplebank.com. (3) Visit your branch and fill out a grievance form. Complaints are acknowledged within 24 hours and resolved within 7-14 working days. If unsatisfied with the resolution, you can escalate to the Banking Ombudsman through the RBI website. Reference number is provided for tracking all complaints.",
    },

    # ===== Accounts =====
    {
        "id": uuid.UUID("d0000002-0000-0000-0000-000000000001"),
        "title": "Savings Account Features",
        "category": "accounts",
        "content": "Our savings accounts offer: (1) Regular Savings: Minimum balance ₹5,000, interest rate 3.5% p.a., free 5 ATM transactions/month, free internet banking. (2) Premium Savings: Minimum balance ₹25,000, interest rate 4.0% p.a., unlimited ATM transactions, priority customer support, complimentary debit card. (3) Zero Balance Savings: No minimum balance, interest rate 3.0% p.a., 3 free ATM transactions/month, basic debit card. All accounts include free NEFT/IMPS transfers up to ₹5 lakhs per month.",
    },
    {
        "id": uuid.UUID("d0000002-0000-0000-0000-000000000002"),
        "title": "Current Account Features",
        "category": "accounts",
        "content": "Current accounts are designed for businesses and professionals: (1) Basic Current: Minimum balance ₹10,000, unlimited transactions, free cheque book (25 leaves/quarter), free demand drafts up to ₹50,000/month. (2) Premium Current: Minimum balance ₹1,00,000, all Basic features plus free RTGS, overdraft facility, dedicated relationship manager. Non-maintenance of minimum balance attracts a charge of ₹500 per quarter.",
    },
    {
        "id": uuid.UUID("d0000002-0000-0000-0000-000000000003"),
        "title": "Fixed Deposit Options",
        "category": "accounts",
        "content": "Fixed deposit tenure options: (1) 7-45 days: 4.5% p.a. (2) 46-90 days: 5.0% p.a. (3) 91-180 days: 5.5% p.a. (4) 181 days to 1 year: 6.0% p.a. (5) 1-2 years: 6.5% p.a. (6) 2-3 years: 6.75% p.a. (7) 3-5 years: 7.0% p.a. (8) 5-10 years: 6.5% p.a. Senior citizens receive an additional 0.50% on all tenures. Premature withdrawal attracts a 1% penalty on the applicable rate. Minimum FD amount is ₹10,000.",
    },
    {
        "id": uuid.UUID("d0000002-0000-0000-0000-000000000004"),
        "title": "Account Closure Process",
        "category": "accounts",
        "content": "To close your account: (1) Visit your home branch with original ID proof. (2) Submit an account closure request form. (3) Return all unused cheque leaves and debit card. (4) Clear any outstanding dues or charges. (5) Remaining balance will be transferred to your specified account or issued as a demand draft. Account closure charges: ₹500 if closed within 1 year of opening, free after 1 year. Processing time: 3-5 working days.",
    },

    # ===== Cards =====
    {
        "id": uuid.UUID("d0000003-0000-0000-0000-000000000001"),
        "title": "Debit Card Types and Features",
        "category": "cards",
        "content": "Debit card variants: (1) Classic Debit Card: Free with savings account, daily ATM limit ₹25,000, daily POS limit ₹50,000, domestic use only. (2) Platinum Debit Card: Annual fee ₹500, daily ATM limit ₹50,000, daily POS limit ₹2,00,000, international usage enabled, airport lounge access (2/quarter). (3) Business Debit Card: For current accounts, daily ATM limit ₹1,00,000, daily POS limit ₹5,00,000. All cards support UPI, contactless payments, and online transactions.",
    },
    {
        "id": uuid.UUID("d0000003-0000-0000-0000-000000000002"),
        "title": "Lost or Stolen Card Procedure",
        "category": "cards",
        "content": "If your card is lost or stolen: (1) IMMEDIATELY call our 24/7 helpline 1800-XXX-XXXX to block the card. (2) You can also block via mobile app: Cards > Block Card. (3) File a written complaint at your branch within 3 days. (4) A replacement card will be issued within 5-7 working days. (5) Replacement fee: ₹200 for Classic, ₹500 for Platinum. (6) Report any unauthorised transactions within 3 days for zero liability protection. Temporary virtual card can be issued via mobile app for immediate online use.",
    },
    {
        "id": uuid.UUID("d0000003-0000-0000-0000-000000000003"),
        "title": "Card PIN Change",
        "category": "cards",
        "content": "To change your debit card PIN: (1) ATM: Insert card > PIN Change > Enter old PIN > Enter new PIN twice. (2) Mobile App: Cards > PIN Management > Generate New PIN. (3) Branch: Fill PIN change request form with valid ID. (4) Net Banking: Cards section > PIN Reset. Green PIN (first-time PIN) is set via SMS or mobile app. PIN must be 4 digits and should not be sequential (1234) or repeated (1111). PIN change is effective immediately.",
    },
    {
        "id": uuid.UUID("d0000003-0000-0000-0000-000000000004"),
        "title": "Credit Card Categories",
        "category": "cards",
        "content": "Credit card options: (1) Silver Card: No annual fee (first year), 1% cashback on all purchases, credit limit ₹50,000-₹2,00,000. (2) Gold Card: Annual fee ₹1,000, 2% cashback, 4 airport lounge visits/year, credit limit ₹2,00,000-₹5,00,000. (3) Platinum Card: Annual fee ₹3,000, 5% cashback on selected categories, unlimited lounge access, concierge service, credit limit ₹5,00,000-₹15,00,000. All cards have a 50-day interest-free period. Late payment fee: ₹500 or 3% of outstanding, whichever is higher.",
    },

    # ===== Fees and Charges =====
    {
        "id": uuid.UUID("d0000004-0000-0000-0000-000000000001"),
        "title": "ATM Transaction Charges",
        "category": "fees",
        "content": "ATM transaction charges: (1) Own bank ATM: First 5 transactions/month free (metro cities) or first 5 transactions (non-metro). After free limit: ₹21 per transaction. (2) Other bank ATM: First 3 transactions/month free (metro) or first 5 (non-metro). After free limit: ₹21 per transaction. (3) Failed ATM transactions due to bank error: No charge, amount refunded within 5 working days. (4) Mini statement at ATM: Free at own ATM, ₹6 at other bank ATM after free limit. All charges are exclusive of GST (18%).",
    },
    {
        "id": uuid.UUID("d0000004-0000-0000-0000-000000000002"),
        "title": "Fund Transfer Charges",
        "category": "fees",
        "content": "Fund transfer charges: (1) UPI: Free for all amounts. (2) IMPS: Up to ₹1 lakh: ₹5, ₹1-2 lakh: ₹15, above ₹2 lakh: ₹25. (3) NEFT: Free for online transfers. Branch NEFT: ₹5 per transaction. (4) RTGS (minimum ₹2 lakh): ₹25 for ₹2-5 lakh, ₹50 for above ₹5 lakh. Online RTGS is free. (5) International wire transfer: ₹500 + correspondent bank charges. All digital transfers through internet or mobile banking are free of charge.",
    },
    {
        "id": uuid.UUID("d0000004-0000-0000-0000-000000000003"),
        "title": "Cheque-Related Charges",
        "category": "fees",
        "content": "Cheque charges: (1) Cheque book: First 25 leaves/quarter free, additional ₹3 per leaf. (2) Cheque return (issuer): ₹350 per cheque for insufficient funds. (3) Cheque return (depositor): ₹100 per cheque. (4) Cheque clearance time: Local cheques: 1-2 working days, outstation cheques: 5-7 working days. (5) Stop payment request: ₹100 per cheque, ₹500 for a range. (6) Demand draft: ₹50 for up to ₹10,000, ₹3 per ₹1,000 thereafter (maximum ₹5,000).",
    },

    # ===== Loans =====
    {
        "id": uuid.UUID("d0000005-0000-0000-0000-000000000001"),
        "title": "Personal Loan Eligibility",
        "category": "loans",
        "content": "Personal loan eligibility: (1) Age: 21-60 years (salaried), 25-65 years (self-employed). (2) Minimum income: ₹25,000/month (salaried), ₹3,00,000/year (self-employed). (3) Employment: Minimum 1 year total experience, 6 months with current employer. (4) Credit score: Minimum 700 (CIBIL). (5) Loan amount: ₹50,000 to ₹25,00,000. (6) Interest rate: 10.5% to 18% p.a. depending on profile. (7) Tenure: 12 to 60 months. (8) Processing fee: 1-2% of loan amount. Documents: Salary slips (3 months), bank statements (6 months), KYC documents.",
    },
    {
        "id": uuid.UUID("d0000005-0000-0000-0000-000000000002"),
        "title": "Home Loan Features",
        "category": "loans",
        "content": "Home loan features: (1) Loan amount: Up to 80% of property value (90% for loans under ₹30 lakh). (2) Interest rate: 8.5% to 10.5% p.a. (floating), 9.5% to 11% (fixed). (3) Tenure: Up to 30 years. (4) Processing fee: 0.5% of loan amount (min ₹10,000, max ₹25,000). (5) Prepayment: No charges for floating rate loans. Fixed rate: 2% of outstanding amount. (6) Tax benefit: Up to ₹2,00,000 on interest (Section 24) and ₹1,50,000 on principal (Section 80C). (7) Top-up loan available after 1 year of regular repayment.",
    },

    # ===== Policies =====
    {
        "id": uuid.UUID("d0000006-0000-0000-0000-000000000001"),
        "title": "Transaction Dispute Policy",
        "category": "policies",
        "content": "Transaction dispute resolution: (1) Report within 30 days of transaction date. (2) Disputes are acknowledged within 24 hours. (3) Provisional credit may be issued within 10 working days for qualifying disputes. (4) Investigation period: Up to 45 days for domestic, 90 days for international. (5) Required information: Transaction reference, date, amount, merchant name, reason for dispute. (6) Dispute categories: Unauthorised transaction, duplicate charge, merchant not delivering goods/services, incorrect amount. (7) Customer zero-liability applies if reported within 3 working days of notification.",
    },
    {
        "id": uuid.UUID("d0000006-0000-0000-0000-000000000002"),
        "title": "Account Dormancy Policy",
        "category": "policies",
        "content": "Account dormancy rules: (1) An account becomes dormant if no customer-initiated transaction occurs for 24 months. (2) Dormant accounts cannot perform debit transactions. (3) To reactivate: Visit the branch with valid KYC documents. (4) Reactivation processing time: 1-3 working days. (5) No charges for reactivation. (6) Interest continues to accrue on dormant savings accounts. (7) If unclaimed for 10 years, the balance is transferred to the RBI's Depositor Education and Awareness Fund (DEAF). (8) DEAF claims can be made through the bank or RBI portal.",
    },
    {
        "id": uuid.UUID("d0000006-0000-0000-0000-000000000003"),
        "title": "KYC and Verification Policy",
        "category": "policies",
        "content": "KYC requirements: (1) Full KYC must be completed within 6 months of account opening. (2) KYC re-verification is required every 2 years for high-risk customers, 8 years for medium-risk, 10 years for low-risk. (3) Acceptable KYC documents: Aadhaar, PAN, Passport, Voter ID, Driving License. (4) Video KYC is available for re-verification. (5) Non-completion of KYC within the deadline results in account restriction (credit-only transactions allowed). (6) Aadhaar-based e-KYC enables instant verification.",
    },
    {
        "id": uuid.UUID("d0000006-0000-0000-0000-000000000004"),
        "title": "Fraud Prevention Guidelines",
        "category": "policies",
        "content": "Protect yourself from fraud: (1) Never share OTP, PIN, or passwords with anyone, including bank employees. (2) The bank will never ask for card details or OTP via call or SMS. (3) Use only official bank app from App Store or Google Play. (4) Enable transaction alerts for all debit and credit transactions. (5) Set daily transaction limits via mobile app. (6) Report suspicious calls/messages to our fraud helpline immediately. (7) Use virtual cards for online purchases. (8) Regularly review your account statements. (9) If you suspect fraud, immediately block your card and call 1800-XXX-XXXX.",
    },

    # ===== Digital Banking =====
    {
        "id": uuid.UUID("d0000007-0000-0000-0000-000000000001"),
        "title": "UPI Payment Service",
        "category": "general",
        "content": "UPI (Unified Payments Interface) features: (1) Instant 24/7 fund transfers. (2) Transaction limit: ₹1,00,000 per transaction. (3) Supported apps: PhonePe, Google Pay, Paytm, BHIM, our bank's mobile app. (4) UPI ID format: mobilenumber@bankname. (5) Scan and pay using QR codes. (6) Recurring payments (autopay) supported. (7) UPI Lite: Pre-loaded wallet for small transactions up to ₹500 without PIN. (8) Transaction charges: Free for all P2P and P2M transactions. (9) Dispute resolution: Within 5 working days for failed/pending transactions.",
    },
    {
        "id": uuid.UUID("d0000007-0000-0000-0000-000000000002"),
        "title": "Mobile Banking App Features",
        "category": "general",
        "content": "Our mobile banking app offers: (1) Account balance and mini statement. (2) Fund transfers (UPI, IMPS, NEFT, RTGS). (3) Bill payments and recharges. (4) Card management (block, unblock, set limits, PIN change). (5) FD/RD booking. (6) Cheque book request. (7) Loan EMI payment. (8) Investment (mutual funds, insurance). (9) QR code payments. (10) Biometric login (fingerprint, face ID). (11) Dark mode support. Download from App Store (iOS) or Google Play (Android). Registration requires linked mobile number and debit card.",
    },
    {
        "id": uuid.UUID("d0000007-0000-0000-0000-000000000003"),
        "title": "Internet Banking Registration",
        "category": "general",
        "content": "To register for internet banking: (1) Visit our website and click 'New User Registration'. (2) Enter your account number and registered mobile number. (3) Verify with OTP sent to registered mobile. (4) Set your login ID and password. (5) Set transaction password. (6) First-time login requires mandatory password change. Requirements: Active savings/current account, registered mobile number, valid debit card. If you face issues, visit your branch with valid ID proof for assisted registration. Internet banking is available for individual and joint accounts.",
    },
]
