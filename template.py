"""
template.py

Run:
    python template.py

This script creates the initial project structure for the
Enterprise Customer Interaction Intelligence Platform.
"""

from pathlib import Path


# ==========================
# Files to Create
# ==========================
FILES = [

    # Root Files
    ".env",
    "README.md",
    "requirements.txt",
    "config.toml",
    "main.py",
    "test-app.py",
    "smoke_test.py",
    "rough.py",

    # Notebook
    "notebooks/customer_interaction_pipeline.ipynb",
    "notebooks/generate_call_recordings.ipynb",

    # Source
    "src/__init__.py",
    "src/config.py",
    "src/logger.py",
    "src/llm_manager.py",
    "src/audio_processor.py",
    "src/document_processor.py",
    "src/cost_tracker.py",
    "src/rate_limiter.py",
    "src/retry_handler.py",
    "src/utils.py",

    # Schemas
    "src/schemas/__init__.py",
    "src/schemas/audio_schema.py",
    "src/schemas/document_schema.py",
    "src/schemas/llm_schema.py",

    # Prompts
    "prompts/audio_prompt.txt",
    "prompts/document_prompt.txt",
]


# ==========================
# Directories to Create
# ==========================
DIRECTORIES = [

    "data/input/audio",
    "data/input/documents",

    "data/output/audio_json",
    "data/output/document_json",

    "data/sample_data",

    "logs",
]


def create_project_structure():
    # Current directory where template.py is located
    root = Path(__file__).parent.resolve()

    # Create Directories
    for directory in DIRECTORIES:
        dir_path = root / directory
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create Files
    for file in FILES:
        file_path = root / file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            if file_path.suffix == ".ipynb":
                file_path.write_text("{}", encoding="utf-8")
            else:
                file_path.touch()

    print("=" * 60)
    print("Project structure created successfully!")
    print(f"Location: {root}")
    print("=" * 60)


if __name__ == "__main__":
    create_project_structure()