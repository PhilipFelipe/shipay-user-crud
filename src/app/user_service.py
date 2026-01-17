from src.domain.user.entity import User
from src.ports.user_repo import UserRepo
from src.utils.password import PasswordHandler


class UserService:
    def __init__(self, user_repository: UserRepo):
        self.user_repository = user_repository

    def create_user(self, user_data: User) -> None:
        password = (
            user_data.password
            if user_data.password
            else PasswordHandler.gen_random_password()
        )
        hash_password = PasswordHandler.hash(password)
        user_data.password = hash_password

        self.user_repository.create_user(**user_data.__dict__)
