import sqlite3
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.app.user_service import UserService
from src.controller.user import get_user_service
from src.infra.sqlite.sqlite_role_adapter import SqliteRoleAdapter
from src.infra.sqlite.sqlite_user_adapter import SqliteUserAdapter
from src.main import app

client = TestClient(app)

conn = sqlite3.connect('test.db', check_same_thread=False)


def override_dependency():
    user_repo_adapter = SqliteUserAdapter(conn)
    role_repo_adapter = SqliteRoleAdapter(conn)
    return UserService(user_repo_adapter, role_repo_adapter)


@pytest.fixture(scope='module')
def setup_db():
    conn.executescript(
        open('src/database/initial.sql', 'r', encoding='utf-8').read()
    )
    conn.executescript(
        open('src/database/test.sql', 'r', encoding='utf-8').read()
    )
    conn.commit()
    yield
    print('Cleaning up test database...')
    conn.execute('DROP TABLE IF EXISTS users;')
    conn.execute('DROP TABLE IF EXISTS roles;')
    conn.commit()
    conn.close()


app.dependency_overrides[get_user_service] = override_dependency


def test_get_user_by_id(setup_db):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@email.com',
        'role_id': 1,
    }


def test_get_users(setup_db):
    response = client.get('/users/')
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


def test_create_user(setup_db):
    new_user = {
        'name': 'Bob Brown',
        'email': 'bob@email.com',
        'password': 'securepassword',
        'role_id': 1,
    }
    response = client.post('/users/', json=new_user)
    assert response.status_code == HTTPStatus.CREATED


def test_create_user_email_conflict(setup_db):
    new_user = {
        'name': 'Billy',
        'email': 'bob@email.com',
        'password': 'securepassword',
        'role_id': 1,
    }

    response = client.post('/users/', json=new_user)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'email indisponível'}


def test_create_user_invalid_password_length(setup_db):
    new_user = {
        'name': 'Carlos',
        'email': 'carlos@email.com',
        'password': '123',
        'role_id': 1,
    }

    response = client.post('/users/', json=new_user)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'senha muito curta, mínimo de 8 caracteres'
    }


def test_update_user_email(setup_db):
    user_update = {
        'email': 'teste2@email.com',
    }
    response = client.patch('/users/1', json=user_update)
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'name': 'John Doe',
        'email': 'teste2@email.com',
        'role_id': 1,
    }


def test_update_user_not_found(setup_db):
    user_update = {'name': 'Teste Atualizado'}
    response = client.patch('/users/999', json=user_update)
    print(response.json())
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_email_conflict(setup_db):
    user_update = {'email': 'teste2@email.com'}
    response = client.patch('/users/2', json=user_update)
    print(response.json())
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'email indisponível'}
