from typing import Optional

from src.domain.user.exceptions import InvalidPasswordLengthException


class User:
    __password_minimum_length = 8

    def __init__(
        self,
        name: str,
        email: str,
        id: Optional[int],
        password: Optional[str],
        role_id: int,
    ):
        # @TODO verificar imeplementação de value object para password aqui
        self.__validate_password(password)

        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id

    name: str
    email: str
    role_id: int
    password: Optional[str]
    id: Optional[int]

    @staticmethod
    def __validate_password(password: Optional[str]) -> None:
        if not password:
            return
        if len(password) < User.__password_minimum_length:
            raise InvalidPasswordLengthException()


class UserFactory:
    @staticmethod
    def create(
        name: Optional[str] = None,
        email: Optional[str] = None,
        role_id: Optional[int] = None,
        id: Optional[int] = None,
        password: Optional[str] = None,
    ) -> User:
        return User(
            id=id, name=name, email=email, password=password, role_id=role_id
        )
