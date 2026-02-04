from http import HTTPStatus

import aiosqlite
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.app.role_service import RoleService
from src.controller.role import get_role_service
from src.infra.sqlite.sqlite_role_adapter import SqliteRoleAdapter
from src.main import app


@pytest_asyncio.fixture(scope='module')
async def setup_db():
    async with aiosqlite.connect('test.db') as db:
        await db.executescript(
            open(
                'src/database/sqlite/initial.sql', 'r', encoding='utf-8'
            ).read()
        )
        await db.executescript(
            open('src/database/sqlite/test.sql', 'r', encoding='utf-8').read()
        )
        await db.commit()

    yield

    async with aiosqlite.connect('test.db') as db:
        await db.execute('DROP TABLE IF EXISTS users;')
        await db.execute('DROP TABLE IF EXISTS roles;')
        await db.commit()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac


async def override_dependency():
    async with aiosqlite.connect('test.db') as conn:
        role_repo_adapter = SqliteRoleAdapter(conn)
        yield RoleService(role_repo_adapter)


app.dependency_overrides[get_role_service] = override_dependency


async def test_get_role_by_id_success(client, setup_db):
    response = await client.get('/roles/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'description': 'default',
    }


async def test_get_role_by_id_not_found_returns_not_found(client, setup_db):
    response = await client.get('/roles/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'role não encontrado'}


async def test_create_role_success(setup_db, client):
    new_role = {
        'description': 'test',
    }
    response = await client.post('/roles/', json=new_role)
    assert response.status_code == HTTPStatus.CREATED


async def test_get_roles_success(setup_db, client):
    response = await client.get('/roles/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': 1,
            'description': 'default',
        },
        {
            'id': 2,
            'description': 'test',
        },
    ]
