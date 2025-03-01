import os

from dotenv import load_dotenv

load_dotenv()


# webhook configurations
WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = os.environ.get("WEB_SERVER_PORT")
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")
BASE_WEBHOOK_URL = os.environ.get("HOST_NAME")
CERT_PATH = os.environ.get("CERT_PATH")
CERT_KEY = os.environ.get("CERT_KEY")

TG_TOKEN_API = os.environ.get("TG_TOKEN_API")
