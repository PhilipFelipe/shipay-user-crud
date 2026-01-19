from typing import Optional

from src.domain.user.exceptions import InvalidPasswordLengthException
from src.utils.password import PasswordHandler


class User:
    __password_minimum_length = 8

    def __init__(
        self,
        name: str,
        email: str,
        id: int,
        password: Optional[str],
        role_id: int,
    ):
        self.__check_password(password)

        self.id = id
        self.name = name
        self.email = email
        self.role_id = role_id

    name: str
    email: str
    role_id: int
    id: int
    _hashed_password: Optional[bytes] = None

    @property
    def password(self) -> bytes:
        return self._hashed_password

    def __check_password(self, password: Optional[str]) -> None:
        if not password:
            self._hashed_password = PasswordHandler.hash(
                PasswordHandler.gen_random_password()
            )
            return
        if len(password) >= User.__password_minimum_length:
            self._hashed_password = PasswordHandler.hash(password)
            return
        raise InvalidPasswordLengthException()


class UserFactory:
    @staticmethod
    def create(
        name: str,
        email: str,
        role_id: int,
        id: int = 0,
        password: Optional[str] = None,
    ) -> User:
        return User(
            id=id, name=name, email=email, password=password, role_id=role_id
        )
