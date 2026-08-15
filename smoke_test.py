from src.document_processor import document_processor
from src.llm_manager import llm
from src.schemas.document_schema import InvoiceDetails
from src.schemas.llm_schema import TopicExplanation

SYSTEM_PROMPT = """
You are a helpful AI assistant.
"""

USER_PROMPT = """
Explain what is a ATM reconciliation is exactly in five bullet points.
"""

def test_structured_output():

    response = llm.chat_completion(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=USER_PROMPT,
        response_format=TopicExplanation,
    )

    structured_output = response["content"]

    print("Structured output:")
    print(f"Topic       : {structured_output.topic}")
    print(f"Explanation : {structured_output.explanation}")
    print("\nApplications:")
    for application in structured_output.applications:
        print(f"- {application}")

def test_document_inference():

    with open("prompts/document_prompt.txt", "r", encoding="utf-8") as file:
        document_prompt = file.read()

    response = document_processor.process_document(
        file_path="data/input/documents/sample_invoice.pdf",
        prompt=document_prompt,
        response_schema=InvoiceDetails
    )

    invoice = response["content"]

    print("\n" + "=" * 80)
    print("DOCUMENT INFERENCE")
    print("=" * 80)

    print(f"Vendor Name   : {invoice.vendor_name}")
    print(f"Invoice No.   : {invoice.invoice_number}")
    print(f"Invoice Date  : {invoice.invoice_date}")
    print(f"Total Amount  : {invoice.total_amount}")

def test_audio_inference():
    pass

def main():
    # test_structured_output()
    # test_document_inference()
    test_audio_inference()    


if __name__ == "__main__":
    main()