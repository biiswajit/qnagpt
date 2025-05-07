from botocore.exceptions import ClientError
import json

# Ensure the bucket exists and is public
def create_bucket(client, bucket_name):
    try:
        client.head_bucket(Bucket=bucket_name)
    except ClientError:
        client.create_bucket(Bucket=bucket_name)
    # Set bucket policy to public
    public_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }]
    }
    client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(public_policy)
    )