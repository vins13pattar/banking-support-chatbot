"""Utility functions for masking sensitive data."""

def mask_account_number(account_number: str) -> str:
    """Masks an account number, keeping only the last 4 digits.
    
    If the account number is already masked or too short, returns as is.
    """
    if len(account_number) <= 4 or "X" in account_number:
        return account_number
    return f"XXXX-XXXX-{account_number[-4:]}"


def mask_phone_number(phone_number: str) -> str:
    """Masks a phone number, keeping only the last 4 digits."""
    if len(phone_number) <= 4 or "X" in phone_number:
        return phone_number
    return f"XXXX-XX-{phone_number[-4:]}"
