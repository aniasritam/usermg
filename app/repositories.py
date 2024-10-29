import boto3
from botocore.exceptions import ClientError
from app.settings import settings
from app.models import User
from uuid import uuid4

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=settings.DYNAMODB_ENDPOINT,
    region_name="us-east-1",
)

table = dynamodb.Table(settings.TABLE_NAME)

class UserRepository:
    @staticmethod
    def create_user(user: User) -> User:
        user.id=uuid4()
        table.put_item(Item=user.dict())
        return user

    @staticmethod
    def get_user(user_id: str) -> User:
        response = table.get_item(Key={"id": user_id})
        user = response.get("Item")
        if not user:
            raise Exception("User not found")
        return User(**user)

    @staticmethod
    def update_user(user_id: str, user: User) -> User:
        response = table.update_item(
            Key={"id": user_id},
            UpdateExpression="SET #name = :name, #email = :email, #role = :role, #number = :number",
            ExpressionAttributeNames={
                "#name": "name",
                "#email": "email",
                "#role": "role",
                "#number": "number"
            },
            ExpressionAttributeValues={
                ":name": user.name,
                ":email": user.email,
                ":role": user.role,
                ":number": user.number,
            },
            ReturnValues="UPDATED_NEW",
        )
        updated_user = response.get("Attributes")
        if not updated_user:
            raise Exception("User not found")
        return User(**updated_user)

    @staticmethod
    def delete_user(user_id: str):
        response = table.delete_item(Key={"id": user_id})
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
            raise Exception("User not found")
