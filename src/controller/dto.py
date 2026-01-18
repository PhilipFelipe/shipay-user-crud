from pydantic import BaseModel, EmailStr


class UserCreateDTOInput(BaseModel):
    name: str
    password: str | None = None
    email: EmailStr
    role_id: int = 1


class UserDTOOutput(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int


class RoleCreateDTOInput(BaseModel):
    name: str
    description: str
