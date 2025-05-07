import boto3
from config.env import get_env

envs = get_env()

def get_s3_client():
  client = boto3.client(
    "s3",
    endpoint_url=envs["s3_endpoint_url"],
    aws_access_key_id=envs["aws_access_key_id"],
    aws_secret_access_key=envs["aws_secret_access_key"],
    region_name=envs["aws_region_name"]
  )
  return client
