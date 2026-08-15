from pydantic import BaseModel, Field


class CustomerCallSummary(BaseModel):
    """
    Structured output for customer support call analysis.
    """

    customer_name: str = Field(
        description="Customer's name, if mentioned"
    )

    issue_category: str = Field(
        description="Primary issue discussed in the call"
    )

    summary: str = Field(
        description="Short summary of the conversation"
    )

    resolution: str = Field(
        description="Final resolution or action taken"
    )

    sentiment: str = Field(
        description="Overall customer sentiment"
    )