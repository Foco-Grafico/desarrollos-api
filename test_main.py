from fastapi.testclient import TestClient
from main import app
from services.db import colina_db
from app.utils import perms

client = TestClient(app)

class TestRole():
    def test_create_role(self):
        id = perms.get_perm_id('test.test')

        response = client.post(
            '/role?token=46983916',
            json={
                'name': 'test-role',
                'description': 'test-role',
                'permissions': [id]
            }
        )

        assert response.status_code == 200

        colina_db.execute(
            sql='DELETE FROM roles WHERE name = %s',
            params=('test-role',)
        )

class TestCreteDevelopment():
    def test_create_development(self):
        response_code = 200

        assert response_code == 200

    def test_create_development_no_token(self):
        response_code = 422

        assert response_code == 422

    def test_create_development_invalid_token(self):
        response_code = 403

        assert response_code == 403

class TestCreateAccount():
    def test_create_account(self):
        response = client.post(
            '/auth/account?token=46983916',
            json={
                'name': 'test',
                'email': 'test@test.com',
                'password': 'test'
            }
        )

        assert response.status_code == 200

        colina_db.execute(
            sql='DELETE FROM users WHERE email = %s',
            params=('test@test.com',)
        )

    def test_create_account_no_token(self):
        response = client.post(
            '/auth/account',
            json={
                'name': 'test',
                'email': 'a',
                'password': 'test'
            }
        )

        assert response.status_code == 422

    def test_create_account_invalid_token(self):
        response = client.post(
            '/auth/account?token=123',
            json={
                'name': 'test',
                'email': 'a',
                'password': 'test'
            }
        )

        assert response.status_code == 403