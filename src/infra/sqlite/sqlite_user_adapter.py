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
        query = """
            SELECT id, name, email, role_id FROM users
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        users: List[User] = []
        for row in rows:
            user = UserFactory.create(
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
        user = UserFactory.create(
            id=row[0],
            name=row[1],
            email=row[2],
            role_id=row[3],
        )
        return user

    def delete_user(self, user_id: int) -> bool:
        query = 'DELETE FROM users WHERE id = ?'
        cursor = self.db_connection.cursor()
        cursor.execute(query, (user_id,))
        self.db_connection.commit()
        return not cursor.rowcount == 0

    def update_user(self, user_id: int, user: User) -> User | None:
        set_clauses = []
        values = []

        if user.name:
            set_clauses.append('name = ?')
            values.append(user.name)
        if user.email:
            set_clauses.append('email = ?')
            values.append(user.email)
        if user.role_id:
            set_clauses.append('role_id = ?')
            values.append(user.role_id)

        set_clause_sql = ', '.join(set_clauses)
        query = f"""
            UPDATE users
            SET {set_clause_sql}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            RETURNING id, name, email, role_id
        """
        cursor = self.db_connection.cursor()
        cursor.execute(
            query,
            (*values, user_id),
        )
        row = cursor.fetchone()
        if not row:
            return None
        user = UserFactory.create(
            id=row[0],
            name=row[1],
            email=row[2],
            role_id=row[3],
        )
        self.db_connection.commit()
        return user

    def user_email_exists(self, email: str) -> bool:
        query = 'SELECT 1 FROM users WHERE email = ?'
        cursor = self.db_connection.cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        return row is not None
