from pathlib import Path
import os

import toml
from dotenv import load_dotenv

class Config:
    """
    Loads project configuration from .env and config.toml .
    """

    def __init__(self):

        # access project root while running this file code
        # .parent for src .parent for parent of src
        self.PROJECT_ROOT = Path(__file__).resolve().parent.parent

        # Load enviornment variables
        load_dotenv(self.PROJECT_ROOT / ".env")

        # Load TOML COnfigurations
        self.config = toml.load(self.PROJECT_ROOT / "config.toml")

        # env variables
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in .env")

        # model configuration
        self.MODELS = self.config["models"]

        # retry configuration
        self.RETRY = self.config["retry"]

        # rate limit configuration
        self.RATE_LIMIT = self.config["rate_limit"]

        # token limit configuration
        self.TOKEN_LIMIT = self.config["token_limit"]

        # cost tracking
        self.COST = self.config["cost"]

        # logging
        self.LOGGING = self.config["logging"]

        # Project Paths
        self.PATHS = self.config["paths"]

config = Config()