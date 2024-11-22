# utils/s3_upload.py

import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def upload_file_to_s3(s3_client, bucket, key, file_content):
    try:
        # Завантаження файлу до S3
        s3_client.put_object(Bucket=bucket, Key=key, Body=file_content)

        # Генерація presigned URL
        file_url = get_presigned_url(s3_client, bucket, key)
        return file_url
    except NoCredentialsError:
        logging.error("AWS credentials not available")
        return None
    except ClientError as e:
        logging.error(f"Client error: {e}")
        return None

def get_presigned_url(s3_client, bucket, key, expiration=3600):
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiration  # Час життя посилання в секундах
        )
        return url
    except ClientError as e:
        logging.error(f"Error generating presigned URL: {e}")
        return None
