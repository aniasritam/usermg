from app.models import User,UserUpdate
from app.repositories import UserRepository
from app.schemas import UserResponse

class UserService:
    @staticmethod
    def create_user(user: User) -> User:
        return UserRepository.create_user(user)

    @staticmethod
    def get_user(email: str) -> User:
        return UserRepository.get_user(email)

    @staticmethod
    def update_user(email: str, user: UserUpdate) -> UserUpdate:
        return UserRepository.update_user(email, user)

    @staticmethod
    def delete_user(email: str):
        UserRepository.delete_user(email)
