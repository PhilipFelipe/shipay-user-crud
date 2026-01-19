from unittest.mock import Mock

import pytest

from src.app.user_service import UserService
from src.domain.user.exceptions import UserEmailAlreadyInUseException


def test_create_user_with_existing_email_raises_exception():
    user_repo = Mock()
    role_repo = Mock()

    user_repo.user_email_exists.return_value = True

    service = UserService(user_repo, role_repo)
    user = Mock()
    user.email = 'existing@example.com'

    with pytest.raises(UserEmailAlreadyInUseException):
        service.create_user(user)
