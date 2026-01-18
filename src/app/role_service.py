from domain.role.entity import Role
from domain.role.exceptions import RoleNotFoundException
from ports.role_repo import RoleRepo
from ports.role_usecases import RoleUsecases


class RoleService(RoleUsecases):
    def __init__(self, role_reposiory: RoleRepo) -> None:
        self.role_reposiory = role_reposiory

    def create_role(self, role_data: Role) -> None:
        self.user_repository.create_user(role_data)

    def get_all_roles(self) -> list[Role]:
        return self.role_reposiory.get_all_roles()

    def get_role_by_id(self, role_id: int) -> Role | None:
        role = self.role_reposiory.get_role_by_id(role_id)
        if not role:
            raise RoleNotFoundException()
        return role
