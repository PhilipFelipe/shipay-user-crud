from http import HTTPStatus

import aiosqlite
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.app.user_service import UserService
from src.controller.user import get_user_service
from src.infra.sqlite.sqlite_role_adapter import SqliteRoleAdapter
from src.infra.sqlite.sqlite_user_adapter import SqliteUserAdapter
from src.main import app


@pytest_asyncio.fixture(scope='module')
async def setup_db():
    async with aiosqlite.connect('test.db') as db:
        await db.executescript(
            open('src/database/initial.sql', 'r', encoding='utf-8').read()
        )
        await db.executescript(
            open('src/database/test.sql', 'r', encoding='utf-8').read()
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
        user_repo_adapter = SqliteUserAdapter(conn)
        role_repo_adapter = SqliteRoleAdapter(conn)
        yield UserService(user_repo_adapter, role_repo_adapter)


app.dependency_overrides[get_user_service] = override_dependency


async def test_get_user_by_id_success(setup_db, client):
    response = await client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@email.com',
        'role_id': 1,
    }


async def test_get_users_success(setup_db, client):
    response = await client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@email.com',
            'role_id': 1,
        },
        {
            'id': 2,
            'name': 'Jane Smith',
            'email': 'jane@email.com',
            'role_id': 1,
        },
        {
            'id': 3,
            'name': 'Alice Johnson',
            'email': 'alice@email.com',
            'role_id': 1,
        },
    ]


async def test_create_user_success(setup_db, client):
    new_user = {
        'name': 'Bob Brown',
        'email': 'bob@email.com',
        'password': 'securepassword',
        'role_id': 1,
    }
    response = await client.post('/users/', json=new_user)
    assert response.status_code == HTTPStatus.CREATED


async def test_create_user_email_conflict_returns_conflict(setup_db, client):
    new_user = {
        'name': 'Billy',
        'email': 'bob@email.com',
        'password': 'securepassword',
        'role_id': 1,
    }

    response = await client.post('/users/', json=new_user)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'email indisponível'}


async def test_create_user_invalid_password_length_returns_bad_request(
    setup_db, client
):
    new_user = {
        'name': 'Carlos',
        'email': 'carlos@email.com',
        'password': '123',
        'role_id': 1,
    }

    response = await client.post('/users/', json=new_user)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'senha muito curta, mínimo de 8 caracteres'
    }


async def test_update_user_email_success(setup_db, client):
    user_update = {
        'email': 'teste2@email.com',
    }
    response = await client.patch('/users/1', json=user_update)
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'name': 'John Doe',
        'email': 'teste2@email.com',
        'role_id': 1,
    }


async def test_update_inexistent_user_returns_not_found(setup_db, client):
    user_update = {'name': 'Teste Atualizado'}
    response = await client.patch('/users/999', json=user_update)
    print(response.json())
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_update_user_existing_email_returns_conflict(setup_db, client):
    user_update = {'email': 'teste2@email.com'}
    response = await client.patch('/users/2', json=user_update)
    print(response.json())
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'email indisponível'}
