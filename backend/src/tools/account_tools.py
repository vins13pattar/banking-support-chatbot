"""Account-related tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.services.account_service import check_account_balance, get_customer_accounts


class GetCustomerAccountsInput(BaseModel):
    customer_id: str = Field(description="The UUID of the verified customer")


@tool("get_customer_accounts", args_schema=GetCustomerAccountsInput)
def get_customer_accounts_tool(customer_id: str) -> dict:
    """Get a list of all accounts belonging to the customer. 
    Use this to find account IDs and masked account numbers.
    """
    accounts = get_customer_accounts(customer_id)
    if not accounts:
        return {"status": "error", "message": "No accounts found for this customer."}
    
    return {
        "status": "success",
        "accounts": [
            {
                "account_id": str(acc.id),
                "account_number_masked": acc.account_number_masked,
                "account_type": acc.account_type,
                "status": acc.status,
            }
            for acc in accounts
        ]
    }


class GetAccountBalanceInput(BaseModel):
    customer_id: str = Field(description="The UUID of the verified customer")
    account_id: str = Field(description="The UUID of the account to check")


@tool("get_account_balance", args_schema=GetAccountBalanceInput)
def get_account_balance_tool(customer_id: str, account_id: str) -> dict:
    """Get the available balance and status for a specific account.
    Fails if the account does not belong to the customer.
    """
    balance_info = check_account_balance(account_id, customer_id)
    if balance_info:
        return {"status": "success", "data": balance_info}
    return {"status": "error", "message": "Account not found or access denied."}
