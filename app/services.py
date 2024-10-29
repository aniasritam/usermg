from app.models import User
from app.repositories import UserRepository

class UserService:
    @staticmethod
    def create_user(user: User) -> User:
        return UserRepository.create_user(user)

    @staticmethod
    def get_user(user_id: str) -> User:
        return UserRepository.get_user(user_id)

    @staticmethod
    def update_user(user_id: str, user: User) -> User:
        return UserRepository.update_user(user_id, user)

    @staticmethod
    def delete_user(user_id: str):
        UserRepository.delete_user(user_id)
