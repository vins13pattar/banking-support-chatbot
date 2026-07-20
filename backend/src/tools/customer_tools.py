"""Customer and authentication tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.services.customer_service import verify_customer, get_customer_by_number
from src.services.masking import mask_phone_number


class VerifyCustomerInput(BaseModel):
    customer_number: str = Field(description="The customer's bank ID/number (e.g., CUST-1001)")
    dob: str = Field(description="Date of birth in YYYY-MM-DD format")
    last_4_phone: str = Field(description="Last 4 digits of the registered phone number")


@tool("verify_customer", args_schema=VerifyCustomerInput)
def verify_customer_tool(customer_number: str, dob: str, last_4_phone: str) -> dict:
    """Verify a customer's identity using their DOB and last 4 digits of their phone number.
    Returns the customer profile on success, or an error message on failure.
    """
    customer = verify_customer(customer_number, dob, last_4_phone)
    if customer:
        return {
            "status": "success",
            "customer_id": str(customer.id),
            "customer_number": customer.customer_number,
            "full_name": customer.full_name,
            "phone_masked": mask_phone_number(customer.phone_masked),
        }
    return {"status": "error", "message": "Verification failed. Invalid customer number, DOB, or phone digits."}


class GetCustomerProfileInput(BaseModel):
    customer_number: str = Field(description="The customer's bank ID/number")


@tool("get_customer_profile", args_schema=GetCustomerProfileInput)
def get_customer_profile_tool(customer_number: str) -> dict:
    """Get a customer's basic profile information. Does NOT authenticate them."""
    customer = get_customer_by_number(customer_number)
    if customer:
        return {
            "status": "success",
            "customer_number": customer.customer_number,
            "full_name": customer.full_name,
            "verification_status": customer.verification_status,
        }
    return {"status": "error", "message": "Customer not found."}
