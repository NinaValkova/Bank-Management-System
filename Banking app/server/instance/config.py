from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:nina2000@localhost/bankdb"
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = "super-secret-key-change-this"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)

JWT_TOKEN_BLOCKLIST_ENABLED = True
JWT_TOKEN_BLOCKLIST_TOKEN_CHECKS = ["access"]


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL")
