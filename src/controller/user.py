import sqlite3
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.app.user_service import UserService
from src.controller.dto import UserCreateDTOInput
from src.domain.user.entity import UserFactory
from src.domain.user.exceptions import InvalidPasswordLengthException
from src.infra.sqlite.sqlite_user_adapter import SqliteUserAdapter

router = APIRouter(prefix='/users')


def get_user_service() -> UserService:
    return UserService(SqliteUserAdapter(sqlite3.connect('users.db')))


@router.post('/', status_code=HTTPStatus.CREATED)
def create_user(
    user: UserCreateDTOInput,
    service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        domain_user = UserFactory.create_user(
            name=user.name,
            email=user.email,
            password=user.password,
            role_id=user.role_id,
        )
        service.create_user(domain_user)
    except InvalidPasswordLengthException as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )
