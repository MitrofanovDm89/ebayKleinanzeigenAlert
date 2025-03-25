import os
import logging


class Settings:
    TOKEN = os.environ.get("TOKEN") or "8028085053:AAHcrxENfsIp1t-GUgkgE-KLKPFDP8upCT0"
    CHAT_ID = os.environ.get("CHAT_ID") or "485186967"
    FILE_LOCATION = os.path.join(os.path.expanduser("~"), "ebayklein.db")
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=HTML&"""
    LOGGING = os.environ.get("LOGGING") or logging.ERROR
    URL_BASE = "https://www.kleinanzeigen.de"


settings = Settings()
