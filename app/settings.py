import os

class Settings:
    DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://localhost:4566")
    TABLE_NAME = os.getenv("TABLE_NAME", "User")

settings = Settings()
