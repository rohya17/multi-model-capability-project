from pydantic import BaseModel, Field

class InvoiceDetails(BaseModel):
    """
    structured output for invoice extraction.
    """

    invoice_number: str = Field(
        description="Invoice number"
    )

    invoice_date: str = Field(
        description="Invoice date"
    )

    vendor_name: str = Field(
            description="Vendor or company name"
        )
    
    total_amount: str = Field(
        description="Total invoice amount"
    )