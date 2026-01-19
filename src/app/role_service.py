from src.domain.role.entity import Role
from src.domain.role.exceptions import RoleNotFoundException
from src.ports.role.role_repo import RoleRepo
from src.ports.role.role_usecases import RoleUsecases


class RoleService(RoleUsecases):
    def __init__(self, role_repository: RoleRepo) -> None:
        self.role_repository = role_repository

    async def create_role(self, role_data: Role) -> None:
        await self.role_repository.create_role(role_data)

    async def get_all_roles(self) -> list[Role]:
        return await self.role_repository.get_all_roles()

    async def get_role_by_id(self, role_id: int) -> Role | None:
        role = await self.role_repository.get_role_by_id(role_id)
        if not role:
            raise RoleNotFoundException()
        return role
