from openai import OpenAI

from src.config import config
from src.retry_handler import retry
from src.rate_limiter import rate_limiter
from src.cost_tracker import cost_tracker
from src.logger import logger

class LLMManager:
    """
    Centralized OpenAI inference manager.

    All interactions with OpenAI should go through this class.
    """

    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)


    # text completion
    @retry
    def chat_completion(self, system_prompt:str, user_prompt:str, response_format=None):
        """
        Performs standard chat completion.
        """
        messages =[
            {
                "role":"system",
                "content":system_prompt
            },
            {
                "role":"system",
                "content":user_prompt
            }
        ]

        rate_limiter.wait_if_needed()

        logger.info("Started text completion request.")

        # structured output or normal output

        if response_format:

            response = self.client.responses.parse(
                model=config.MODELS["document_model"],
                input=str(messages),
                text_format=response_format,
            )

            content = response.output_parsed

        else:

            response = self.client.responses.create(
                model=config.MODELS["document_model"],
                input=str(messages),
                temperature=config.MODELS["temperature"],
                max_output_tokens=config.MODELS["max_tokens"],
            )

            content = response.output_text

        logger.info("Text completion request completed.")

        usage = response.usage

        cost = cost_tracker.calculate_cost(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens
        )

        logger.info(
            f"Model={config.MODELS['document_model']} | "
            f"Input Tokens={cost['input_tokens']} | "
            f"Output Tokens={cost['output_tokens']} | "
            f"Total cost={cost['current_total_cost']} {cost['currency']} | "
        )

        return {
            "success": True,
            "content": content,
            "usage": cost,
            "model": config.MODELS["document_model"],
        }

    # Audio completion
    @retry
    def audio_completion(self, messages):
        """
        Performs an audio completion request.

        Parameters
        messages : list
            OpenAI chat Completion messages containing
            input_audio + prompt.

        Returns
        dict
            standardized response object.
        """

        rate_limiter.wait_if_needed()

        logger.info("Starting audio completion request.")

        response = self.client.chat.completions.create(
            model=config.MODELS["audio_model"],
            temperature=config.MODELS["temperature"],
            messages=messages
        )

        logger.info("Text completion request completed.")
        
        usage = response.usage

        cost = cost_tracker.calculate_cost(
            input_tokens=usage.input_tokens if hasattr(usage,"input_tokens") else usage.prompt_tokens,
            output_tokens=usage.output_tokens if hasattr(usage,"input_tokens") else usage.completion_tokens
        )

        logger.info(
            f"Model={config.MODELS['audio_model']} | "
            f"Input Tokens={cost['input_tokens']} | "
            f"Output Tokens={cost['output_tokens']} | "
            f"Total cost={cost['current_total_cost']} {cost['currency']} | "
        )

        return {
            "Success":True,
            "content":response.choices[0].message.content,
            "usage":cost,
            "model": config.MODELS["audio_model"]
        }

llm = LLMManager()