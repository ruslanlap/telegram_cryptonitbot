#!/bin/bash

# # Встановлюємо ім'я головної папки
# PROJECT_NAME="CryptonitBot"

# # Створюємо головну папку
# mkdir -p "$PROJECT_NAME"

# # Переходимо до головної папки
# cd "$PROJECT_NAME" || exit

# Створюємо основні файли
touch main.py config.py keyboards.py states.py requirements.txt Instructions.txt

# Створюємо папку handlers та необхідні файли всередині
mkdir -p handlers
touch handlers/__init__.py handlers/start.py handlers/encrypt.py handlers/decrypt.py

# Створюємо папку utils та необхідні файли всередині
mkdir -p utils
touch utils/__init__.py utils/encryption.py utils/s3_upload.py

echo "Структура проекту '$PROJECT_NAME' успішно створена."
