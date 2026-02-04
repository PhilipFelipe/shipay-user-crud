from typing import List, Optional

from src.domain.user.entity import User, UserFactory
from src.infra.postgres.db import PostgresDatabase
from src.ports.user.user_repo import UserRepo


class PostgresUserAdapter(UserRepo):
    def __init__(self, db: PostgresDatabase) -> None:
        self.db = db

    async def create_user(self, user: User) -> None:
        query = """
            INSERT INTO users (
                name, email, password, role_id, created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        async with self.db.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    query, (user.name, user.email, user.password, user.role_id)
                )
            await conn.commit()

    async def get_all_users(self) -> List[User]:
        query = """
            SELECT id, name, email, role_id FROM users
        """
        async with self.db.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                rows = await cur.fetchall()

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
            SELECT id, name, email, role_id FROM users WHERE id = %s
        """
        async with self.db.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (user_id,))
                row = await cur.fetchone()
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
        query = 'DELETE FROM users WHERE id = %s'
        async with self.db.connection() as conn:
            deleted = False
            async with conn.cursor() as cur:
                await cur.execute(query, (user_id,))
                deleted = not cur.rowcount == 0
            await conn.commit()
            return deleted

    async def update_user(self, user_id: int, user: User) -> User | None:
        set_clauses = []
        values = []

        if user.name:
            set_clauses.append('name = %s')
            values.append(user.name)
        if user.email:
            set_clauses.append('email = %s')
            values.append(user.email)
        if user.role_id:
            set_clauses.append('role_id = %s')
            values.append(user.role_id)

        set_clause_sql = ', '.join(set_clauses)
        query = f"""
            UPDATE users
            SET {set_clause_sql}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, name, email, role_id
        """
        async with self.db.connection() as conn:
            updated_user = None
            async with conn.cursor() as cur:
                await cur.execute(
                    query,
                    (*values, user_id),
                )
                row = await cur.fetchone()
                if not row:
                    return None
                updated_user = UserFactory.create(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role_id=row[3],
                )
            await conn.commit()
            return updated_user

    async def get_user_by_email(self, email: str) -> User | None:
        query = 'SELECT id, name, email, role_id FROM users WHERE email = %s'
        async with self.db.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (email,))
                row = await cur.fetchone()
                if not row:
                    return None
                user = UserFactory.create(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    role_id=row[3],
                )
                return user
