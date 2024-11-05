import boto3
from fastapi import HTTPException
from botocore.exceptions import ClientError
from app.settings import settings
from app.models import User, UserUpdate
from boto3.dynamodb.conditions import Key
from uuid import uuid4
from pydantic import ValidationError, BaseModel, Field
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=settings.DYNAMODB_ENDPOINT,
)

table = dynamodb.Table(settings.TABLE_NAME)


class UserRepository:
    
    @staticmethod
    def create_user(user: User):
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
              raise HTTPException(status_code=400, detail="User with this email already exists")

              
          # Assign a unique ID if validation passes
          user_id = str(uuid4())
          user_data['id'] = user_id
          
          # Attempt to save the user to DynamoDB
          table.put_item(Item=user.dict())
        #   print(f"User {user.id} created successfully")
          
          return user_data
      
      except ValidationError as ve:
        
          raise ValidationError("User data validation failed: Missing required fields") from ve

     
      except HTTPException as he:
        # Specific handling for HTTP exceptions
        raise he
      
      

    @staticmethod
    def get_user(email: str):
        try:
            response = table.get_item(Key={"email": email})
            print(response)
            user = response.get("Item")
            
            # Raise ValueError if the user is not found
            if not user:
                raise ValueError("User not found")
            
            return user
        
        except ValueError as ve:
            # Handle specific ValueError for user not found
            print(f"Error: {ve}")
            raise  # Re-raise the exception if necessary
        

   

    @staticmethod
    def update_user(email: str, user: UserUpdate) -> UserUpdate:
      try:
        
        existing_user_response = table.get_item(Key={"email": email})
        existing_user = existing_user_response.get("Item")
            
        if not existing_user:
            raise ValueError("User not found")  # More specific exception
        
        response = table.update_item(
        Key={"email": email},
        UpdateExpression="SET #name = :name, #role = :role, #number = :number",
        ExpressionAttributeNames={
        "#name": "name",
        
        "#role": "role",
        "#number": "number"
        },
        ExpressionAttributeValues={
                    ":name": user.name,
                
                    ":role": user.role,
                    ":number": user.number,
                },
                ReturnValues="UPDATED_NEW",
            )
          
        updated_user = response.get("Attributes")
          
        if not updated_user:
          raise ValueError("User not found")  # More specific exception

        return UserUpdate(**updated_user)
      
      

      except ValueError as ve:
          # Specific handling for user not found
          print(f"Update User Error: {ve}")
          raise ve
      
      
    @staticmethod
    def delete_user(email: str):
        try:
            existing_user_response = table.get_item(Key={"email": email})
            existing_user = existing_user_response.get("Item")
            
            if not existing_user:
               raise ValueError("User not found")  # More specific exception
            

            response = table.delete_item(Key={"email": email})

            # Check if the deletion was successful
            if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
                raise ValueError("User not found or could not be deleted.")
        except ValueError as ve:
            # Specific handling for user not found
            print(f"Delete User Error: {ve}")
            raise ve

       

        
        