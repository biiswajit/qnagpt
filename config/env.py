from dotenv import load_dotenv
import os

load_dotenv() # load environment variables

def get_env():
  return {
    "mistralai_api_key" : os.getenv("MISTRALAI_API_KEY"),
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID") or "test",
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY") or "test",
    "aws_region_name": os.getenv("AWS_REGION") or "us-east-1",
    "environment": os.getenv("ENVIRONMENT") or "development",
    "bucket_name_for_pdfs": os.getenv("PDF_UPLOAD_BUCKET_NAME") or "docs",
    "s3_endpoint_url": os.getenv("S3_ENDPOINT_URL") or "http://localhost:4566"
  }