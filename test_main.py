from fastapi.testclient import TestClient
from main import app
from services.db import colina_db

client = TestClient(app)

class TestAccount():
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