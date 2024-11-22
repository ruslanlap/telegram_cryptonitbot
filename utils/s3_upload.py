# utils/s3_upload.py
import io
import logging
import boto3
from botocore.exceptions import NoCredentialsError

def upload_file_to_s3(s3_client, bucket, key, file_content):
    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body=file_content)
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False

def get_presigned_url(s3_client, bucket, key, expiration=3600):
            try:
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket,
                        'Key': key,
                    },
                    ExpiresIn=expiration,
                    HttpMethod='GET'
                )
                return url
            except Exception as e:
                print(f"Error generating presigned URL: {e}")
                return None