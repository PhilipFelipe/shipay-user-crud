from sqlite3 import Connection

from src.ports.user_repo import UserRepo


class SqliteUserAdapter(UserRepo):
    def __init__(self, db_connection: Connection):  # add type here
        self.db_connection = db_connection

    def create_user(
        self, name: str, email: str, password: str, role_id: int
    ) -> None:
        query = """
            INSERT INTO users (name, email, password, role_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (name, email, password, role_id))
        self.db_connection.commit()
