from typing import Protocol

from src.domain.user.entity import User


class UserRepo(Protocol):
    def create_user(self, user: User) -> None: ...

    def get_all_users(self) -> list[User]: ...

    def get_user_by_id(self, user_id: int) -> User | None: ...
