from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, EmailStr


def empty_email_validator(value: str) -> str:
    if not value:
        return None
    return value


class UserCreateDTOInput(BaseModel):
    name: str
    email: EmailStr
    password: Optional[str] = None
    role_id: Optional[int] = 1


class UserDTOOutput(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int


class UserUpdateDTOInput(BaseModel):
    name: Optional[str] = None
    email: Annotated[
        Optional[EmailStr], BeforeValidator(empty_email_validator)
    ] = None
    role_id: Optional[int] = None


class RoleCreateDTOInput(BaseModel):
    description: str


class RoleDTOOutput(BaseModel):
    id: int
    description: str
