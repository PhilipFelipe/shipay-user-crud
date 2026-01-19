from typing import Protocol

from src.domain.role.entity import Role


class RoleRepo(Protocol):
    async def create_role(self, role: Role) -> None: ...

    async def get_all_roles(self) -> list[Role]: ...

    async def get_role_by_id(self, role_id: int) -> Role | None: ...
