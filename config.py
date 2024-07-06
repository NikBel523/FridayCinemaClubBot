import os


# webhook configurations
WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8000
WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = "https://cinemabot.strangled.net"


TG_TOKEN_API = os.environ.get("TG_TOKEN_API")
