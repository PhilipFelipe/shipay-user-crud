import sqlite3
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.app.role_service import RoleService
from src.controller.role import get_role_service
from src.infra.sqlite.sqlite_role_adapter import SqliteRoleAdapter
from src.main import app

client = TestClient(app)

conn = sqlite3.connect('test.db', check_same_thread=False)


def override_dependency():
    role_repo_adapter = SqliteRoleAdapter(conn)
    return RoleService(role_repo_adapter)


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


app.dependency_overrides[get_role_service] = override_dependency


def test_get_role_by_id_success(setup_db):
    response = client.get('/roles/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'description': 'default',
    }


def test_get_role_by_id_not_found_returns_not_found(setup_db):
    response = client.get('/roles/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'role não encontrado'}


def test_create_role_success(setup_db):
    new_role = {
        'description': 'test',
    }
    response = client.post('/roles/', json=new_role)
    assert response.status_code == HTTPStatus.CREATED


def test_get_roles_success(setup_db):
    response = client.get('/roles/')
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
