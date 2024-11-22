# tests/conftest.py
import pytest
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import boto3
from config import BOT_TOKEN, AWS_S3_BUCKET
from unittest.mock import patch

@pytest.fixture
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def s3_client_mock():
    with mock_s3():
        # Налаштування мок S3
        s3 = boto3.client('s3', region_name='eu-north-1')
        s3.create_bucket(Bucket=AWS_S3_BUCKET)
        yield s3

@pytest.fixture
def bot():
    return Bot(token=BOT_TOKEN)

@pytest.fixture
def dp(bot):
    storage = MemoryStorage()
    dispatcher = Dispatcher(bot, storage=storage)
    return dispatcher

@pytest.fixture
def mock_upload_file_to_s3():
    with patch('utils.s3_upload.upload_file_to_s3') as mock_upload:
        mock_upload.return_value = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/decrypted_messages/test.txt"
        yield mock_upload

@pytest.fixture
def mock_decrypt():
    with patch('utils.encryption.decrypt') as mock_decrypt_func:
        mock_decrypt_func.return_value = "Decrypted message"
        yield mock_decrypt_func

@pytest.fixture
def mock_escape_markdown_v2():
    with patch('utils.encryption.escape_markdown_v2') as mock_escape:
        mock_escape.return_value = "Decrypted message"
        yield mock_escape
