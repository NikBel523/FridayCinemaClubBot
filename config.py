import os

from dotenv import load_dotenv

load_dotenv()


TG_TOKEN_API = os.environ.get("TG_TOKEN_API")
BOT_MODE = os.environ.get("BOT_MODE", "polling").lower()  # polling or webhook

# Webhook
WEB_SERVER_HOST = os.environ.get("WEB_SERVER_HOST", "127.0.0.1")
WEB_SERVER_PORT = int(os.environ.get("WEB_SERVER_PORT", 443))
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH", "/webhook")
BASE_WEBHOOK_URL = os.environ.get("HOST_NAME")
CERT_PATH = os.environ.get("CERT_PATH")
CERT_KEY = os.environ.get("CERT_KEY")

if BOT_MODE == "webhook":
    if not all([BASE_WEBHOOK_URL, CERT_PATH, CERT_KEY]):
        raise ValueError("Для webhook режима необходимо указать HOST_NAME, CERT_PATH и CERT_KEY")
    WEBHOOK_FULL_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
else:
    WEBHOOK_FULL_URL = None