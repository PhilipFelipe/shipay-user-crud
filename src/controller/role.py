import sqlite3
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from src.app.role_service import RoleService
from src.controller.dto import RoleCreateDTOInput, RoleDTOOutput
from src.domain.role.entity import RoleFactory
from src.domain.role.exceptions import RoleNotFoundException
from src.infra.sqlite.sqlite_role_adapter import SqliteRoleAdapter

router = APIRouter(prefix='/roles')


def get_role_service() -> RoleService:
    connection = sqlite3.connect('users.db')
    role_repo_adapter = SqliteRoleAdapter(connection)
    return RoleService(role_repo_adapter)


@router.post('/', status_code=HTTPStatus.CREATED)
def create_role(
    role: RoleCreateDTOInput,
    service: Annotated[RoleService, Depends(get_role_service)],
):
    try:
        domain_role = RoleFactory.create(
            description=role.description,
        )
        service.create_role(domain_role)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get('/{role_id}', response_model=RoleDTOOutput)
def get_role(
    role_id: int,
    service: Annotated[RoleService, Depends(get_role_service)],
):
    try:
        role = service.get_role_by_id(role_id)
        return role.__dict__
    except RoleNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='role não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get('/', response_model=List[RoleDTOOutput])
def list_roles(
    service: Annotated[RoleService, Depends(get_role_service)],
):
    try:
        roles = service.get_all_roles()
        return [role.__dict__ for role in roles]
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )
