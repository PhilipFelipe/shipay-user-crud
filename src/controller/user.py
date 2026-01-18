import sqlite3
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from src.app.user_service import UserService
from src.controller.dto import (
    UserCreateDTOInput,
    UserDTOOutput,
)
from src.domain.user.entity import UserFactory
from src.domain.user.exceptions import (
    InvalidPasswordLengthException,
    UserNotFoundException,
)
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


@router.get('/{user_id}', response_model=UserDTOOutput)
def get_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        user = service.get_user_by_id(user_id)
        return user.__dict__
    except UserNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get('/', response_model=List[UserDTOOutput] | None)
def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        users = service.get_all_users()
        return [user.__dict__ for user in users]
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )
