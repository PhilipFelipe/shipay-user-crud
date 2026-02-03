from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiosqlite import Connection, connect


class SqliteDatabase:
    def __init__(self):
        self._db_path = 'users.db'

    @asynccontextmanager
    async def connection(
        self,
    ) -> AsyncGenerator[Connection]:
        conn = await connect(self._db_path)
        try:
            yield conn
        except Exception as e:
            print('[DB_ERROR] - {}'.format(e))
            raise
        finally:
            await conn.close()
