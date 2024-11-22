# config.py
import os
import boto3
from botocore.config import Config  # Правильний імпорт Config
from dotenv import load_dotenv

load_dotenv()  # Завантаження змінних середовища з .env файлу

BOT_TOKEN = os.getenv('YOUR_BOT_TOKEN')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

# Створення конфігурації
aws_config = Config(
    signature_version='s3v4',
    region_name='eu-north-1'  # або ваш регіон
)

# Ініціалізація S3 клієнта
s3_client = boto3.client(
    's3',
aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=aws_config
)

aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')

if not BOT_TOKEN:
    raise ValueError("Не вказано токен бота. Будь ласка, встановіть змінну середовища YOUR_BOT_TOKEN.")
if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET]):
    raise ValueError("Не вказані AWS credentials або S3 бакет. Будь ласка, встановіть змінні середовища AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY та AWS_S3_BUCKET.")





    