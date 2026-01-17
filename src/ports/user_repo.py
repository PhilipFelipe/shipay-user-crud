from typing import Protocol


class UserRepo(Protocol):
    def create_user(
        self, name: str, email: str, password: str, role_id: int
    ) -> None: ...
