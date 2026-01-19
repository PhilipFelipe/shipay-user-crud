from src.domain.role.exceptions import RoleNotFoundException
from src.domain.user.entity import User
from src.domain.user.exceptions import (
    UserEmailAlreadyInUseException,
    UserNotFoundException,
)
from src.ports.role.role_repo import RoleRepo
from src.ports.user.user_repo import UserRepo
from src.ports.user.user_usecases import UserUsecases


class UserService(UserUsecases):
    def __init__(
        self, user_repository: UserRepo, role_reposiory: RoleRepo
    ) -> None:
        self.user_repository = user_repository
        self.role_reposiory = role_reposiory

    async def create_user(self, user_data: User) -> None:
        if await self.user_repository.get_user_by_email(user_data.email):
            raise UserEmailAlreadyInUseException()
        await self.user_repository.create_user(user_data)

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.user_repository.delete_user(user_id)
        if not deleted:
            raise UserNotFoundException()

    async def update_user(self, user_id: int, user_data: User) -> User:
        if user_data.email:
            existing_user = await self.user_repository.get_user_by_email(
                user_data.email
            )
            if existing_user and existing_user.id != user_id:
                raise UserEmailAlreadyInUseException()
        if user_data.role_id:
            role = await self.role_reposiory.get_role_by_id(user_data.role_id)
            if not role:
                raise RoleNotFoundException()

        user = await self.user_repository.update_user(user_id, user_data)
        if not user:
            raise UserNotFoundException()
        return user
