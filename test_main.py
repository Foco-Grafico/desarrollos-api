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

class TestPaymentPlan():
    def test_create_payment_plan(self):
        response = client.post(
            '/payment?token=46983916',
            json={
                'price': 1,
                'months_to_pay': 3,
                'annuity': 1,
                'pay_per_month': 5,
                'interest_rate': 90,
                'payment_method': 'cola'
            }
        )

        assert response.status_code == 200

        plan_id = response.json()['plan_id']

        colina_db.execute(
            sql='DELETE FROM payment_plans WHERE id = %s',
            params=(plan_id,)
        )

class TestBatch():
    @pytest.mark.asyncio
    async def test_create_batch(self):
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

        with open('test_assets/foco.png', 'rb') as png, open('test_assets/foco.svg', 'rb') as svg:
            files = [
                ('assets', ('foco.png', png)),
                ('assets', ('foco.svg', svg))
            ]

            res = client.post(
                '/batch?token=46983916',
                files=files,
                data={
                    'area': '90',
                    'perimeter': '90',
                    'longitude': '90',
                    'coords': 'cooooooords',
                    'amenities': 'amenities',
                    'price': '90',
                    'development_id': dev_id
                }
            )

        assert res.status_code == 200

        await delete_dev(development_id=dev_id, token='46983916')

    @pytest.mark.asyncio
    async def test_delete_batch(self):
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

        with open('test_assets/foco.png', 'rb') as png, open('test_assets/foco.svg', 'rb') as svg:
            files = [
                ('assets', ('foco.png', png)),
                ('assets', ('foco.svg', svg))
            ]

            batch_id = client.post(
                '/batch?token=46983916',
                files=files,
                data={
                    'area': '90',
                    'perimeter': '90',
                    'longitude': '90',
                    'coords': 'cooooooords',
                    'amenities': 'amenities',
                    'price': '90',
                    'development_id': dev_id
                }
            ).json()['batch_id']

        res = client.delete(
            f'/batch?token=46983916&id={batch_id}'
        )

        assert res.status_code == 200

        await delete_dev(development_id=dev_id, token='46983916')
    
    @pytest.mark.asyncio
    async def test_batch_assing_asset(self):
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

        with open('test_assets/foco.png', 'rb') as png, open('test_assets/foco.svg', 'rb') as svg:
            files = [
                ('assets', ('foco.png', png)),
                ('assets', ('foco.svg', svg))
            ]

            batch_id = client.post(
                '/batch?token=46983916',
                files=files,
                data={
                    'area': '90',
                    'perimeter': '90',
                    'longitude': '90',
                    'coords': 'cooooooords',
                    'amenities': 'amenities',
                    'price': '90',
                    'development_id': dev_id
                }
            ).json()['batch_id']


        res = client.post(
            f'/batch/assign/asset?token=46983916&batch_id={batch_id}',
            json={
                'asset_url': 'https://blogs.21rs.es/corazones/files/2015/06/si.png'
            }
        )

        assert res.status_code == 200

        await delete_dev(development_id=dev_id, token='46983916')

    @pytest.mark.asyncio
    async def test_batch_assign_payment_plant(self):
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

        with open('test_assets/foco.png', 'rb') as png, open('test_assets/foco.svg', 'rb') as svg:
            files = [
                ('assets', ('foco.png', png)),
                ('assets', ('foco.svg', svg))
            ]

            batch_id = client.post(
                '/batch?token=46983916',
                files=files,
                data={
                    'area': '90',
                    'perimeter': '90',
                    'longitude': '90',
                    'coords': 'cooooooords',
                    'amenities': 'amenities',
                    'price': '90',
                    'development_id': dev_id
                }
            ).json()['batch_id']

        plan_id = client.post(
            '/payment?token=46983916',
            json={
                'price': 1,
                'months_to_pay': 3,
                'annuity': 1,
                'pay_per_month': 5,
                'interest_rate': 90,
                'payment_method': 'cola'
            }
        ).json()['plan_id']

        res = client.post(
            f'/batch/assign/payment-plan?token=46983916&batch_id={batch_id}&plan_id={plan_id}',
        )

        assert res.status_code == 200

        await delete_dev(development_id=dev_id, token='46983916')