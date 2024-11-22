# Telegram Bot with AWS S3 Integration on Aiogram

<p align="center">
  <img src="/data/bot.png" width="100" />
</p>
<p align="center">
    <h1 align="center">AWS-Enabled Telegram Bot</h1>
</p>
<p align="center">
    <em>A Telegram bot built using Aiogram for efficient interaction with AWS S3 services.</em>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
</p>
<hr>

## 🔗 Quick Links
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [🚀 Getting Started](#-getting-started)
  - [⚙️ Installation](#️-installation)
  - [🤖 Running the Bot](#-running-the-bot)
- [🛠 Environment Variables](#-environment-variables)
- [⚙️ AWS Configuration](#%EF%B8%8F-aws-configuration)
- [📂 Project Structure](#-project-structure)
- [📄 License](#-license)

---

## 📍 Overview Updates for CryptonitBot_V2 

This bot utilizes:
- **Aiogram** for handling Telegram bot updates.
- **AWS S3** for file storage and retrieval.
- **FSM Storage** for managing user state.
- [Previous version here](https://github.com/ruslanlap/Cryptonit-BOT)

---

## 📦 Features

- **Telegram Interaction**:
  - Handles commands and unknown messages.
  - Provides a custom keyboard with options.
  - Aiogram with async instead Telegram Telebot.

- **Bot with accessible structure**:
  - Instead of one file, the functions are separated and structured.

- **AWS S3 Integration**:
  - File uploads and downloads.
  - Secure interaction using access keys.

- **Error Handling**:
  - Logs detailed errors for debugging.

---

## 🚀 Getting Started

### ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ruslanlap/telegram_cryptonitbot
   cd telegram_cryptonitbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and define your environment variables:
   ```bash
   YOUR_BOT_TOKEN=<your-telegram-bot-token>
   AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
   AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
   AWS_S3_BUCKET=<your-s3-bucket-name>
   ```

---

### 🤖 Running the Bot

1. Start the bot:
   ```bash
   python main.py
   ```

2. Interact with the bot via Telegram. Type `/start` to initiate.

---

## 🛠 Environment Variables

- `BOT_TOKEN`: Telegram Bot API token from BotFather.
- `AWS_ACCESS_KEY_ID`: AWS IAM user's access key.
- `AWS_SECRET_ACCESS_KEY`: AWS IAM user's secret access key.
- `AWS_S3_BUCKET`: AWS S3 bucket name.

> Ensure these values are securely stored and not exposed.

---

## ⚙️ AWS Configuration

To securely configure AWS permissions for your Telegram bot to interact with AWS S3:

1. **Policy Configuration**:
   Create or attach the following policy for the IAM user. Replace `<YOUR_IAM_NAME>` and `<YOUR_S3_BUCKET>` with your IAM username and S3 bucket name.

   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "Allow<YOUR_IAM_NAME>Operations",
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::961341510486:user/<YOUR_IAM_NAME>"
               },
               "Action": [
                   "s3:PutObject",
                   "s3:GetObject"
               ],
               "Resource": [
                   "arn:aws:s3:::<YOUR_S3_BUCKET>/encrypted_messages/*",
                   "arn:aws:s3:::<YOUR_S3_BUCKET>/decrypted_messages/*"
               ]
           }
       ]
   }
   ```

2. **Attach Policy to IAM User**:
   - Go to the AWS Management Console.
   - Navigate to **IAM > Users > <YOUR_IAM_NAME> > Permissions**.
   - Attach the custom policy created above.

3. **Testing the Configuration**:
   Use the bot to upload and download files, ensuring no permission errors.

---

## 📂 Project Structure

```sh
CryptonitBot_V2/
├── main.py
├── config.py
├── handlers/
│   ├── __init__.py
│   ├── start.py
│   ├── encrypt.py
│   └── decrypt.py
├── utils/
│   ├── __init__.py
│   ├── encryption.py
│   └── s3_upload.py
├── keyboards.py
├── states.py
├── requirements.txt
└── Instructions.txt
```

---

## 📄 License

This project is licensed under the MIT License.
