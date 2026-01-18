from sqlite3 import Connection
from typing import List, Optional

from src.domain.user.entity import User, UserFactory
from src.ports.user_repo import UserRepo


class SqliteUserAdapter(UserRepo):
    def __init__(self, db_connection: Connection) -> None:
        self.db_connection = db_connection

    def create_user(self, user: User) -> None:
        query = """
            INSERT INTO users (
                name, email, password, role_id, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        cursor = self.db_connection.cursor()
        cursor.execute(
            query, (user.name, user.email, user.password, user.role_id)
        )
        self.db_connection.commit()

    def get_all_users(self) -> List[User]:
        breakpoint()
        query = """
            SELECT id, name, email, role_id FROM users
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        users: List[User] = []
        for row in rows:
            user = UserFactory.create_user(
                id=row[0],
                name=row[1],
                email=row[2],
                role_id=row[3],
            )
            users.append(user)
        return users

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = """
            SELECT id, name, email, role_id FROM users WHERE id = ?
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        user = UserFactory.create_user(
            id=row[0],
            name=row[1],
            email=row[2],
            role_id=row[3],
        )
        return user
