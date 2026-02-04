from typing import List, Optional

from aiosqlite import Connection

from src.domain.role.entity import Role, RoleFactory
from src.ports.role.role_repo import RoleRepo


class SqliteRoleAdapter(RoleRepo):
    def __init__(self, db: Connection) -> None:
        self.db_connection = db

    async def create_role(self, role: Role) -> None:
        query = """
            INSERT INTO roles (
                description
            )
            VALUES (?)
        """
        await self.db_connection.execute(query, (role.description,))
        await self.db_connection.commit()

    async def get_all_roles(self) -> List[Role]:
        query = """
            SELECT id, description FROM roles
        """
        cursor = await self.db_connection.execute(query)
        rows = await cursor.fetchall()

        roles: List[Role] = []
        for row in rows:
            role = RoleFactory.create(
                id=row[0],
                description=row[1],
            )
            roles.append(role)

        return roles

    async def get_role_by_id(self, role_id: int) -> Optional[Role]:
        query = """
            SELECT id, description FROM roles WHERE id = ?
        """
        cursor = await self.db_connection.execute(query, (role_id,))
        row = await cursor.fetchone()
        if not row:
            return None
        role = RoleFactory.create(
            id=row[0],
            description=row[1],
        )
        return role
