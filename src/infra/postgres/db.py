from contextlib import asynccontextmanager
from typing import AsyncGenerator

from psycopg import AsyncConnection, Connection


class PostgresDatabase:
    def __init__(self, db: str, host: str, user: str, pwd: str, port: str):
        self._conn_string = (
            f'host={host} port={port} dbname={db} user={user} password={pwd}'
        )

    @asynccontextmanager
    async def connection(
        self,
    ) -> AsyncGenerator[AsyncConnection]:
        aconn = await AsyncConnection.connect(self._conn_string)
        try:
            yield aconn
        except Exception as e:
            print('[DB_ERROR] - {}'.format(e))
            raise
        finally:
            await aconn.close()

    def apply_initial_migration(self):
        # improvised initial migration apply
        with open('src/database/pg/initial.sql', 'r', encoding='utf-8') as f:
            script_sql = f.read()
            with Connection.connect(self._conn_string) as conn:
                conn.execute(script_sql)
                conn.commit()
            print('[PG] Migração inicial aplicada!')
