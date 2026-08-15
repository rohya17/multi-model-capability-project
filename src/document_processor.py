from pathlib import Path

from openai import OpenAI

from src.config import config
from src.llm_manager import llm
from src.logger import logger

class DocumentProcessor:
    """
    Processes PDF documents using OpenAI's multimodel models.
    """

    SYSTEM_PROMPT = "You are a file parser expert. " \
    "You identify the fields that are required and returns it " \
    "in expected response format."

    def process_document(self, file_path, prompt, response_schema):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"{file_path} not found."
            )

        client = OpenAI(api_key=config.OPENAI_API_KEY)

        uploaded_file = client.files.create(
            file=file_path,
            purpose="user_data"
        )

        user_prompt = [
            {
                "type":"input_file",
                "file_id": uploaded_file.id
            },
            {
                "type":"input_text",
                "text":prompt
            }
        ]

        logger.info(f"Processing document for parsing response {file_path}")

        return llm.chat_completion(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=str(user_prompt),
            response_format=response_schema
        )

document_processor = DocumentProcessor()