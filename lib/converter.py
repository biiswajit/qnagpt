from lib.text_cleaner import clean_text
from lib.parse_pdf import parse_pdf
from config.env import get_env

def convert_from_pdf_to_text() -> str:
  """
  function to convert pdf to text.
  Args:
    path_to_pdf: path to the pdf file.
  Returns:
    str: extracted text
  """
  api_key = get_env()["mistralai_api_key"]
  extracted_text = parse_pdf(api_key)
  cleaned_text = clean_text(extracted_text)
  return cleaned_text