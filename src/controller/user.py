from http import HTTPStatus
from typing import Annotated, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from src.app.user_service import UserService
from src.containers import Container
from src.controller.dto import (
    UserCreateDTOInput,
    UserDTOOutput,
    UserUpdateDTOInput,
)
from src.domain.user.entity import UserFactory
from src.domain.user.exceptions import (
    InvalidPasswordLengthException,
    UserEmailAlreadyInUseException,
    UserNotFoundException,
)

router = APIRouter(prefix='/users')


@router.post('/', status_code=HTTPStatus.CREATED)
@inject
async def create_user(
    user: UserCreateDTOInput,
    service: Annotated[UserService, Depends(Provide[Container.user_svc])],
):
    try:
        domain_user = UserFactory.create(
            name=user.name,
            email=user.email,
            password=user.password,
            role_id=user.role_id,
        )
        await service.create_user(domain_user)
    except UserEmailAlreadyInUseException:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='email indisponível'
        )
    except InvalidPasswordLengthException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='senha muito curta, mínimo de 8 caracteres',
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get('/{user_id}', response_model=UserDTOOutput)
@inject
async def get_user(
    user_id: int,
    service: Annotated[UserService, Depends(Provide[Container.user_svc])],
):
    try:
        user = await service.get_user_by_id(user_id)
        return user.__dict__
    except UserNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get('/', response_model=List[UserDTOOutput])
@inject
async def list_users(
    service: Annotated[UserService, Depends(Provide[Container.user_svc])],
):
    try:
        users = await service.get_all_users()
        return [user.__dict__ for user in users]
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
@inject
async def delete_user(
    user_id: int,
    service: Annotated[UserService, Depends(Provide[Container.user_svc])],
):
    try:
        await service.delete_user(user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch('/{user_id}', response_model=UserDTOOutput)
@inject
async def update_user(
    user_id: int,
    user_update: UserUpdateDTOInput,
    service: Annotated[UserService, Depends(Provide[Container.user_svc])],
):
    try:
        user = UserFactory.create(
            name=user_update.name,
            email=user_update.email,
            role_id=user_update.role_id,
        )
        updated_user = await service.update_user(
            user_id,
            user,
        )
        return updated_user.__dict__
    except UserNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado'
        )
    except UserEmailAlreadyInUseException:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='email indisponível'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )
