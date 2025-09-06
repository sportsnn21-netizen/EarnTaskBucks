import os

class Settings:
    BOT_TOKEN = os.getenv("8338228858:AAH_K8Hm5U5QRDiCiVCD83U_3Oidhw60RsA")
    ADMIN_IDS = list(map(int, os.getenv("5168384940", "").split(",")))
    REQUIRED_CHANNELS = os.getenv("REQUIRED_CHANNELS", "").split(",")
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
