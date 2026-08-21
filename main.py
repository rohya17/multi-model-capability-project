# define import and paths
from pathlib import Path
import sys
from urllib import response
import warnings

from pandas import DataFrame

warnings.filterwarnings("ignore")

# paths
PROJECT_ROOT = Path(__file__).resolve().parent

print(PROJECT_ROOT)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

INPUT_AUDIO_PATH = PROJECT_ROOT / "data" / "input" / "audio"
INPUT_DOCUMENT_DIR = PROJECT_ROOT / "data" / "input" / "documents"
OUTPUT_DATA_DIR = PROJECT_ROOT / "data" / "output"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# more imports

import pandas as pd
from tqdm.auto import tqdm

from src.audio_processor import audio_processor
from src.document_processor import document_processor
from src.schemas.audio_schema import CustomerCallSummary
from src.schemas.document_schema import InvoiceDetails
from src.cost_tracker import cost_tracker
from src import utils

# initialize output dir, audio and document prompt with def

def main():

    try:
        start_time = utils.current_time()
        audio_prompt, document_prompt = initialize()

        audio_df = process_audio_files(audio_prompt)
        document_df = process_transcribed_document(document_prompt)

        print_pipeline_summary(audio_df, document_df)

        elapsed_time = utils.calculate_elapsed_time(start_time)
        print(f"\nPipeline completed successfully in {elapsed_time} seconds.")

    except Exception as e :
        print(f"Pipeline failed : {e}")
        raise

def print_pipeline_summary(audio_df, document_df):
    """Print a combined report covering both pipelines plus API usage/cost."""

    summary = cost_tracker.summary()

    print("\n" + "=" * 60)
    print("Overall Pipeline Summary")
    print("=" * 60)

    print("\nAudio Processing")
    print_summary("Files", audio_df)

    print("\nDocument Processing")
    print_summary("Documents", document_df)

    print("\nAPI Usage")
    print(f"Requests         : {summary['total_requests']}")
    print(f"Input Tokens     : {summary['total_input_tokens']:,}")
    print(f"Output Tokens    : {summary['total_output_tokens']:,}")
    print(f"Total Tokens     : {summary['total_tokens']:,}")
    print(f"Estimated Cost   : ${summary['total_cost']:.6f} {summary['currency']}")

def initialize():
    """Prepares Output Folder and Input Prompts"""

    OUTPUT_DATA_DIR.mkdir(parents=True,exist_ok=True)

    audio_prompt = utils.load_prompt(PROMPTS_DIR / "audio_prompt.txt")
    document_prompt = utils.load_prompt(PROMPTS_DIR / "document_prompt.txt")

    return audio_prompt, document_prompt

def print_summary(label, df):
    """Print a small Total/Successful/Failed report for any results dataframe."""
    completed = (df["status"] == "Completed").sum()
    print(f"\n{label} Pipeline Summary")
    print(f"Total {label} : {len(df)}")
    print(f"Successful : {completed}")
    print(f"Failed : {len(df) - completed}")

def process_audio_files(audio_prompt):
    """Transcribe / Summarize every .wav file and save the results to CSV."""

    print("AP >> Checking for audio files to process....")
    audio_df = utils.discover_files(INPUT_AUDIO_PATH, "call_*.wav")
    print(f"AP >> Found {len(audio_df)} audio files to process.\nAP >> Started Processing....")

    results = []

    for index, row in tqdm(audio_df.iterrows(), total=len(audio_df), desc="Processing Audio FIles..."):
        try:
            response = audio_processor.process_audio(
                file_path=row["file_path"],
                prompt=audio_prompt,
                response_schema=CustomerCallSummary
            )
            results.append(response.model_dump())
            audio_df.loc[index,"status"] = "Completed"

        except Exception as e:
            audio_df.loc[index,"status"] = f"Failed : {e}"
            results.append(
                {
                    "customer_name":None,
                    "issue_category":None,
                    "summary":None,
                    "resolution":None,
                    "sentiment":None
                }
            )

    print("AP >> Audio Files transcribed, putting everything together..")

    final_audio_df = pd.concat([audio_df.reset_index(drop=True),pd.DataFrame(results)], axis=1)

    output_file = OUTPUT_DATA_DIR / "customer_call_analysis.csv"
    utils.save_dataframe(final_audio_df, output_file)

    print(f"AP >> Done .. results saved to : {output_file}")
    print_summary("Audio Files",final_audio_df)

    return final_audio_df

def process_transcribed_document(document_prompt):
    """Extract invoice details from every document and save the results to csv"""

    print("DP >> Searching for transcription documents...")
    document_df = utils.discover_files(INPUT_DOCUMENT_DIR,"*.*")
    print(f"Found {len(document_df)} documents.")

    results = []
    empty_invoice = {
        "invoice_number": None, 
        "invoice_date": None, 
        "vendor_name": None, 
        "total_amount": None
    }

    for index, row in tqdm(document_df.iterrows(), desc="Processing Transcription Documents", total=len(document_df)):
        try:
            response = document_processor.process_document(
                file_path=row["file_path"],
                prompt=document_prompt,
                response_schema=InvoiceDetails
            )

            if response["success"]:
                results.append(response["content"].model_dump())
                document_df.loc[index,"status"] = "Completed"
            else:
                results.append(empty_invoice)
                document_df.loc[index,"status"] = "Failed"

        except Exception as e:
            results.append(empty_invoice)
            document_df.loc[index, "status"] = f"Failed: {e}"

    print("DP >> Putting all together...")

    final_document_df = pd.concat([document_df.reset_index(drop=True), pd.DataFrame(results)], axis=1)
    output_file = OUTPUT_DATA_DIR / "customer_document_analysis.csv"
    utils.save_dataframe(final_document_df, output_file)

    print(f"\nDocument results saved to:\n{output_file}")
    print_summary("Transcription Documents", final_document_df)

    return final_document_df

if __name__ == "__main__":
    main()