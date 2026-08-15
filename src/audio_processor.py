import base64
import json
from pathlib import Path

from src.llm_manager import llm
from src.logger import logger

class AudioProcessor:
    """
    Processes audio files using OpenAI's audio-capable mode;.
    """

    def process_audio(self, file_path, prompt:str, response_schema):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"{file_path} not found."
            )

        logger.info(f"Started processing audio: {file_path.name}")

        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        logger.info("Audio file encoded successfully.")

        messages = [
            {
                "role":"user",
                "content":[
                    {
                        "type":"input_audio",
                        "input_audio": {
                            "data": audio_b64,
                            "format": file_path.suffix.replace(".",""),
                        },
                    },
                    {
                        "type":"text",
                        "text":prompt
                    }
                ]
            }
        ]

        response =llm.audio_completion(messages=messages)

        logger.info("Recieved response from llm.")

        raw_response = response["content"]

        data =json.loads(raw_response)

        normalized_data = {
            "customer_name": data.get("customer_name") or data.get("Customer Name"),
            "issue_category": data.get("issue_category") or data.get("Issue Category"),
            "summary": data.get("summary") or data.get("Summary"),
            "resolution": data.get("resolution") or data.get("Resolution"),
            "sentiment":data.get("sentiment") or data.get("Sentiment")
        }

        parsed_response = response_schema.model_validate(normalized_data)

        logger.info(f"Successfully processed: {file_path.name}")

        return parsed_response

audio_processor = AudioProcessor()

        