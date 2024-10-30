import boto3
from botocore.exceptions import ClientError
from app.settings import settings
from app.models import User, UserUpdate
from boto3.dynamodb.conditions import Key
from uuid import uuid4
from pydantic import ValidationError, BaseModel, Field
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=settings.DYNAMODB_ENDPOINT,
    region_name="us-east-1",
)

table = dynamodb.Table(settings.TABLE_NAME)


class UserRepository:
    
    @staticmethod
    def create_user(user: User) -> User:
      try:
          # Check if required fields are missing using Pydantic validation
          

          user_data = user.dict(exclude_unset=True)  # Validate and convert to dict
          if "name" not in user_data or "email" not in user_data:
              raise ValidationError("Missing required data: username or email")

            # Query the table to check if a user with the same email or username exists
          existing_user = table.get_item(
                Key={"email": user.email}  # Assuming email is the unique key
            ).get('Item')
          if existing_user:
              raise ValueError("User with this email already exists")
              
          # Assign a unique ID if validation passes
          user.id = str(uuid4())
          
          # Attempt to save the user to DynamoDB
          table.put_item(Item=user.dict())
          
          return user
      
      except ValidationError as ve:
          print(f"Validation Error: {ve}")
          raise ValueError("User data validation failed: Missing required fields") from ve

      except ValueError as ve:
          # Specific handling for user already existing
          print(f"User Creation Error: {ve}")
          raise ve
      
      except ClientError as ce:
          # Catching DynamoDB ClientError (network issues, authorization, etc.)
          print(f"DynamoDB Client Error: {ce}")
          raise RuntimeError("An error occurred while saving to DynamoDB") from ce
      
      except Exception as e:
          # Catching any other unexpected exceptions
          print(f"Unexpected Error: {e}")
          raise RuntimeError("An unexpected error occurred") from e

    @staticmethod
    def get_user(user_id: str) -> UserUpdate:
        response = table.get_item(Key={"id": user_id})
        print(response)
        user = response.get("Item")
        if not user:
            raise Exception("User not found")
        return UserUpdate(**user)

    # @staticmethod
    # def update_user(user_id: str, user: UserUpdate) -> UserUpdate:
    #     response = table.update_item(
    #         Key={"id": user_id},
    #         UpdateExpression="SET #name = :name, #email = :email, #role = :role, #number = :number",
    #         ExpressionAttributeNames={
    #             "#name": "name",
    #             "#email": "email",
    #             "#role": "role",
    #             "#number": "number"
    #         },
    #         ExpressionAttributeValues={
    #             ":name": user.name,
    #             ":email": user.email,
    #             ":role": user.role,
    #             ":number": user.number,
    #         },
    #         ReturnValues="UPDATED_NEW",
    #     )
    #     updated_user = response.get("Attributes")
    #     if not updated_user:
    #         raise Exception("User not found")
    #     return User(**updated_user)


    @staticmethod
    def update_user(user_id: str, user: UserUpdate) -> UserUpdate:
      try:
        response = table.update_item(
        Key={"id": id},
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
          raise ValueError("User not found")  # More specific exception

        return User(**updated_user)

      except ValueError as ve:
          # Specific handling for user not found
          print(f"Update User Error: {ve}")
          raise ve
      
      except ValidationError as ve:
          # Handle validation errors for UserUpdate input
          print(f"Validation Error: {ve}")
          raise ValueError("User data validation failed") from ve

      except ClientError as ce:
          # Handle any errors that occur during the DynamoDB operation
          print(f"DynamoDB Client Error: {ce}")
          raise RuntimeError("An error occurred while updating the user in DynamoDB") from ce

      except Exception as e:
          # Catch any other unexpected exceptions
          print(f"Unexpected Error: {e}")
          raise RuntimeError("An unexpected error occurred") from e


    # @staticmethod
    # def delete_user(user_id: str):
    #     response = table.delete_item(Key={"id": user_id})
    #     if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
    #         raise Exception("User not found")
    @staticmethod
    def delete_user(user_id: str):
        try:
            response = table.delete_item(Key={"id": user_id})

            # Check if the deletion was successful
            if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
                raise ValueError("User not found or could not be deleted.")

        except ClientError as ce:
            # Handle any errors that occur during the DynamoDB operation
            print(f"DynamoDB Client Error: {ce}")
            raise RuntimeError("An error occurred while trying to delete the user in DynamoDB") from ce

        except Exception as e:
            # Catch any other unexpected exceptions
            print(f"Unexpected Error: {e}")
            raise RuntimeError("An unexpected error occurred while deleting the user") from e
        