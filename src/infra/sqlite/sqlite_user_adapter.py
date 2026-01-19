from typing import List, Optional

from aiosqlite import Connection

from src.domain.user.entity import User, UserFactory
from src.ports.user_repo import UserRepo


class SqliteUserAdapter(UserRepo):
    def __init__(self, db_connection: Connection) -> None:
        self.db_connection = db_connection

    async def create_user(self, user: User) -> None:
        query = """
            INSERT INTO users (
                name, email, password, role_id, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        await self.db_connection.execute(
            query, (user.name, user.email, user.password, user.role_id)
        )
        await self.db_connection.commit()

    async def get_all_users(self) -> List[User]:
        query = """
            SELECT id, name, email, role_id FROM users
        """
        cursor = await self.db_connection.execute(query)
        rows = await cursor.fetchall()

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

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = """
            SELECT id, name, email, role_id FROM users WHERE id = ?
        """
        cursor = await self.db_connection.execute(query, (user_id,))
        row = await cursor.fetchone()
        if not row:
            return None
        user = UserFactory.create(
            id=row[0],
            name=row[1],
            email=row[2],
            role_id=row[3],
        )
        return user

    async def delete_user(self, user_id: int) -> bool:
        query = 'DELETE FROM users WHERE id = ?'
        cursor = await self.db_connection.execute(query, (user_id,))
        await self.db_connection.commit()
        return not cursor.rowcount == 0

    async def update_user(self, user_id: int, user: User) -> User | None:
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
        cursor = await self.db_connection.execute(
            query,
            (*values, user_id),
        )
        row = await cursor.fetchone()
        if not row:
            return None
        user = UserFactory.create(
            id=row[0],
            name=row[1],
            email=row[2],
            role_id=row[3],
        )
        await self.db_connection.commit()
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        query = 'SELECT id, name, email, role_id FROM users WHERE email = ?'
        cursor = await self.db_connection.execute(query, (email,))
        row = await cursor.fetchone()
        if not row:
            return None
        user = UserFactory.create(
            id=row[0],
            name=row[1],
            email=row[2],
            role_id=row[3],
        )
        return user
