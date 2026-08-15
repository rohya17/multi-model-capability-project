from pydantic import BaseModel, Field


class TopicExplanation(BaseModel):
    """
    Structured response for testing OpenAI Structured Output.
    """

    topic: str = Field(description="Topic being explained")

    explanation: str = Field(
        description="Short explanation of the topic"
    )

    applications: list[str] = Field(
        description="List of real-world applications"
    )