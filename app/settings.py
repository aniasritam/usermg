import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://localhost:4566")
    TABLE_NAME = os.getenv("TABLE_NAME", "User")

settings = Settings()
