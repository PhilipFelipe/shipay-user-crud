from typing import Optional

from src.domain.user.exceptions import InvalidPasswordLengthException


class User:
    __password_minimum_length = 8

    def __init__(
        self,
        id: Optional[int],
        name: str,
        email: str,
        password: Optional[str],
        role_id: int,
    ):
        self.__validate_password(password)

        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id

    name: str
    email: str
    password: Optional[str]
    role_id: int

    @staticmethod
    def __validate_password(password: Optional[str]) -> None:
        if not password:
            return
        if len(password) < User.__password_minimum_length:
            raise InvalidPasswordLengthException()


class UserFactory:
    @staticmethod
    def create_user(
        name: str,
        email: str,
        role_id: int,
        id: Optional[int] = None,
        password: Optional[str] = None,
    ) -> User:
        return User(
            id=id, name=name, email=email, password=password, role_id=role_id
        )
