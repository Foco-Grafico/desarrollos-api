from fastapi.testclient import TestClient
from main import app
from services.db import colina_db
from app.routes.controllers.development.delete import delete_dev
import pytest

client = TestClient(app)

class TestRole():
    def test_create_role(self):
        response = client.post(
            '/role?token=46983916',
            json={
                'name': 'test-role',
                'description': 'test-role',
                'permissions': ['role.delete']
            }
        )

        assert response.status_code == 200

        colina_db.execute(
            sql='DELETE FROM roles WHERE name = %s',
            params=('test-role',)
        )

    def test_add_perm_to_role(self):
        role_id = client.post(
            '/role?token=46983916',
            json={
                'name': 'test-role',
                'description': 'test-role',
                'permissions': ['role.delete']
            }
        ).json()['role_id']
        
        res = client.post(
            f'/role/add-perm?token=46983916&role_id={role_id}&perm_str=role.create',
        )

        assert res.status_code == 200

        colina_db.execute(
            sql='DELETE FROM roles WHERE id = %s',
            params=(role_id,)
        )

class TestDevelopment():
    @pytest.mark.asyncio
    async def test_create_development(self):
        with open('test_assets/foco.png', 'rb') as f:
            files = {'logo': ('foco.png', f)}

            response = client.post(
                '/development?token=46983916',
                data={
                        'name': 'test',
                        'description': 'test',
                        'address': 'test',
                        'city': 'test',
                        'state': 'test',
                        'country': 'test',
                        'contact_number': 'test',
                        'contact_email': 'dsadsa'
                },
                files=files
            )

        assert response.status_code == 200

        dev_id = response.json()['dev_id']

        await delete_dev(development_id=dev_id, token='46983916')

    @pytest.mark.asyncio
    async def test_delete_dev(self):
        with open('test_assets/foco.png', 'rb') as f:
            files = {'logo': ('foco.png', f)}

            dev_id = client.post(
                '/development?token=46983916',
                data={
                        'name': 'test',
                        'description': 'test',
                        'address': 'test',
                        'city': 'test',
                        'state': 'test',
                        'country': 'test',
                        'contact_number': 'test',
                        'contact_email': 'dsadsa'
                },
                files=files
            ).json()['dev_id']

        res = client.delete(
            f'/development?token=46983916&development_id={dev_id}'
        )

        assert res.status_code == 200

    @pytest.mark.asyncio
    async def test_get_dev(self):
        with open('test_assets/foco.png', 'rb') as f:
            files = {'logo': ('foco.png', f)}

            dev_id = client.post(
                '/development?token=46983916',
                data={
                        'name': 'test',
                        'description': 'test',
                        'address': 'test',
                        'city': 'test',
                        'state': 'test',
                        'country': 'test',
                        'contact_number': 'test',
                        'contact_email': 'dsadsa'
                },
                files=files
            ).json()['dev_id']

        res = client.get(
            '/development'
        )

        assert res.status_code == 200

        await delete_dev(development_id=dev_id, token='46983916')

    @pytest.mark.asyncio
    async def test_get_one_dev(self):
        with open('test_assets/foco.png', 'rb') as f:
            files = {'logo': ('foco.png', f)}

            dev_id = client.post(
                '/development?token=46983916',
                data={
                        'name': 'test',
                        'description': 'test',
                        'address': 'test',
                        'city': 'test',
                        'state': 'test',
                        'country': 'test',
                        'contact_number': 'test',
                        'contact_email': 'dsadsa'
                },
                files=files
            ).json()['dev_id']

        res = client.get(
            f'/development/{dev_id}'
        )

        assert res.status_code == 200

        await delete_dev(development_id=dev_id, token='46983916')

    @pytest.mark.asyncio
    async def test_edit_dev(self):
        with open('test_assets/foco.png', 'rb') as f:
            files = {'logo': ('foco.png', f)}

            dev_id = client.post(
                '/development?token=46983916',
                data={
                        'name': 'test',
                        'description': 'test',
                        'address': 'test',
                        'city': 'test',
                        'state': 'test',
                        'country': 'test',
                        'contact_number': 'test',
                        'contact_email': 'dsadsa'
                },
                files=files
            ).json()['dev_id']

        with open('test_assets/foco.svg', 'rb') as f:
            files = {'logo': ('foco.svg', f)}

            res = client.put(
                f'/development/{dev_id}?token=46983916',
                files=files,
                data={
                    'name': 'test2'
                }
            )

        assert res.status_code == 200

        await delete_dev(development_id=dev_id, token='46983916')

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