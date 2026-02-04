from dependency_injector import containers, providers
from dotenv import load_dotenv

from src.app.user_service import UserService

# from src.infra.sqlite.db import SqliteDatabase
from src.infra.postgres.db import PostgresDatabase

# from src.infra.sqlite.sqlite_user_adapter import SqliteUserAdapter
from src.infra.postgres.postgres_user_adapter import PostgresUserAdapter
from src.infra.sqlite.sqlite_role_adapter import SqliteRoleAdapter


class Container(containers.DeclarativeContainer):
    load_dotenv()

    config = providers.Configuration()

    config.postgres.db.from_env('POSTGRES_DB', required=True)
    config.postgres.host.from_env('POSTGRES_HOST', required=True)
    config.postgres.pwd.from_env('POSTGRES_PWD', required=True)
    config.postgres.user.from_env('POSTGRES_USER', required=True)
    config.postgres.port.from_env('POSTGRES_PORT', required=True)

    # SQLITE Adapter
    # db_connection = providers.Singleton(SqliteDatabase)
    # Postgres Adapter
    db = providers.Singleton(PostgresDatabase, **config.postgres())

    user_repo_adapter = providers.Factory(PostgresUserAdapter, db=db)
    user_role_adapter = providers.Factory(
        SqliteRoleAdapter, db=db.provided.connection
    )

    user_svc = providers.Factory(
        UserService,
        user_repository=user_repo_adapter,
        role_reposiory=user_role_adapter,
    )
