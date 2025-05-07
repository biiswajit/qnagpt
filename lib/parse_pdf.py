from mistralai import Mistral

def parse_pdf(api_key: str) -> str:
    """
    Performs OCR on a given PDF file and returns cleaned text.
    Args:
        pdf_path (str): Path to the PDF file.
        api_key (str): Mistral API key.
    Returns:
        str: Cleaned text extracted from the PDF.
    """
    client = Mistral(api_key=api_key)
    # Upload PDF
    with open("./book.pdf", "rb") as f:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": "book.pdf".split("/")[-1],
                "content": f,
            },
            purpose="ocr"
        )
    # Get signed URL
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
    # OCR Processing
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        }
    )
    # Join extracted markdown
    extracted_text = "\n\n".join([page.markdown for page in ocr_response.pages])
    return extracted_text