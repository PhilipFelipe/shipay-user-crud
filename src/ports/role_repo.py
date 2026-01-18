from typing import Protocol

from src.domain.role.entity import Role


class RoleRepo(Protocol):
    def create_role(self, role: Role) -> None: ...

    def get_all_roles(self) -> list[Role]: ...

    def get_role_by_id(self, role_id: int) -> Role | None: ...
