from dependency_injector import containers, providers

from src.app.user_service import UserService
from src.infra.sqlite.db import SqliteDatabase
from src.infra.sqlite.sqlite_role_adapter import SqliteRoleAdapter
from src.infra.sqlite.sqlite_user_adapter import SqliteUserAdapter


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_connection = providers.Singleton(SqliteDatabase)

    user_repo_adapter = providers.Factory(
        SqliteUserAdapter, db_connection=db_connection.provided.connection
    )
    user_role_adapter = providers.Factory(
        SqliteRoleAdapter, db_connection=db_connection.provided.connection
    )

    user_svc = providers.Factory(
        UserService,
        user_repository=user_repo_adapter,
        role_reposiory=user_role_adapter,
    )
