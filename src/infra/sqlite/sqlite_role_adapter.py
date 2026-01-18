from sqlite3 import Connection
from typing import List, Optional

from src.domain.role.entity import Role, RoleFactory
from src.ports.role_repo import RoleRepo


class SqliteRoleAdapter(RoleRepo):
    def __init__(self, db_connection: Connection) -> None:
        self.db_connection = db_connection

    def create_role(self, role: Role) -> None:
        query = """
            INSERT INTO roles (
                description
            )
            VALUES (?)
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (role.description,))
        self.db_connection.commit()

    def get_all_roles(self) -> List[Role]:
        query = """
            SELECT id, description FROM roles
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        roles: List[Role] = []
        for row in rows:
            role = RoleFactory.create(
                id=row[0],
                description=row[1],
            )
            roles.append(role)
        return roles

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        query = """
            SELECT id, description FROM roles WHERE id = ?
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (role_id,))
        row = cursor.fetchone()
        if not row:
            return None
        role = RoleFactory.create(
            id=row[0],
            description=row[1],
        )
        return role
