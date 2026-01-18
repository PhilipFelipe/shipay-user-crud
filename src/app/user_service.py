from src.domain.role.exceptions import RoleNotFoundException
from src.domain.user.entity import User
from src.domain.user.exceptions import (
    UserEmailAlreadyInUseException,
    UserNotFoundException,
)
from src.ports.role_repo import RoleRepo
from src.ports.user_repo import UserRepo
from src.ports.user_usecases import UserUsecases
from src.utils.password import PasswordHandler


class UserService(UserUsecases):
    def __init__(
        self, user_repository: UserRepo, role_reposiory: RoleRepo
    ) -> None:
        self.user_repository = user_repository
        self.role_reposiory = role_reposiory

    def create_user(self, user_data: User) -> None:
        if self.user_repository.user_email_exists(user_data.email):
            raise UserEmailAlreadyInUseException()

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

    def delete_user(self, user_id: int) -> None:
        deleted = self.user_repository.delete_user(user_id)
        if not deleted:
            raise UserNotFoundException()

    def update_user(self, user_id: int, user_data: User) -> User:
        if user_data.email:
            existing_user = self.user_repository.user_email_exists(
                user_data.email
            )
            if existing_user:
                raise UserEmailAlreadyInUseException()
        if user_data.role_id:
            role = self.role_reposiory.get_role_by_id(user_data.role_id)
            if not role:
                raise RoleNotFoundException()

        user = self.user_repository.update_user(user_id, user_data)
        if not user:
            raise UserNotFoundException()
        return user
