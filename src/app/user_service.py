from src.domain.user.entity import User
from src.domain.user.exceptions import UserNotFoundException
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

        self.user_repository.create_user(user_data)

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
