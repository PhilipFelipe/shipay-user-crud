from unittest.mock import AsyncMock

import pytest

from src.app.user_service import UserService
from src.domain.user.exceptions import UserEmailAlreadyInUseException


async def test_create_user_with_existing_email_raises_exception():
    user_repo = AsyncMock()
    role_repo = AsyncMock()

    user_repo.get_user_by_email.return_value = True

    service = UserService(user_repo, role_repo)
    user = AsyncMock()
    user.email = 'existing@example.com'

    with pytest.raises(UserEmailAlreadyInUseException):
        await service.create_user(user)
