import pytest

from src.domain.user.entity import UserFactory
from src.domain.user.exceptions import InvalidPasswordLengthException
from src.utils.password import PasswordHandler


def test_user_entity_creation_invalid_password_length():
    with pytest.raises(InvalidPasswordLengthException):
        UserFactory.create(
            name='John Doe',
            email='john.doe@example.com',
            role_id=1,
            password='short',
        )


def test_user_entity_creation_valid_password_length():
    user = UserFactory.create(
        name='Jane Doe',
        email='jane.doe@example.com',
        role_id=2,
        password='validpassword',
    )
    assert PasswordHandler.verify('validpassword', user.password) is True
