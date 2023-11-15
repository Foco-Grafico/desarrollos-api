from mysqlclientpy import DB
from dotenv import load_dotenv
import os
import math
load_dotenv()

class Env():
    @staticmethod
    def get(key):
        return os.environ.get(key)
    
    @staticmethod
    def get_secure(key):
        value = Env.get(key)

        if value is None:
            raise Exception(f'Environment variable {key} is not set')
        
        return value

colina_db = DB(
    database=Env.get_secure('NAME_DB'),
    host=Env.get_secure('HOST_DB'),
    password=Env.get_secure('PASS_DB'),
    user=Env.get_secure('USER_DB')
)

def create_devs(num_devs: int):
    for i in range(num_devs):
        dev_data = {
            'name': f'Desarrollo {i+1}',
            'description': f'Descripcion del desarrollo {i+1}',
            'address': f'Direccion del desarrollo {i+1}',
            'city': f'Ciudad del desarrollo {i+1}',
            'state': f'Estado del desarrollo {i+1}',
            'country': f'Pais del desarrollo {i+1}',
            'logo_url': 'public/colina.svg',
            'contact_number': '1234567890',
            'contact_email': 'contact@colina.com'
        }
        print(f'Creating development {i+1}...')

        colina_db.insert(table='developments', data=dev_data)

def create_batches(num_batch_per_dev: int):
    devs = colina_db.select(table='developments', columns=['id'])

    currecies = ['MXN', 'USD', 'EUR', 'CAD', 'GBP', 'JPY', 'CNY', 'CHF', 'AUD', 'NZD']
    status = [1, 2, 3]

    for dev in devs:
        for i in range(num_batch_per_dev):
            payment_plan = {
                'months_to_pay': i+1*3,
                'interest_rate': 0.1,
                'annuity': i+1*math.pi,
                'pay_per_month': (i+1*math.pi)/12,
                'payment_method': 'payment_method',
                'price': 100000,
            }

            print(f'Creating payment plan {i+1} for development {dev["id"]}...')

            payment_plan_id = colina_db.insert(table='payment_plans', data=payment_plan)

            batch_data = {
                'area': 100,
                'price': 100000,
                'perimeter': 100,
                'longitude': 100,
                'coords': 'coords',
                'development_id': dev['id'],
                'currency': currecies[i % len(currecies)],
                'location': 'location',
                'sq_m': 100,
                'amenities': 'amenities',
                'sides': 4,
                'status': status[i % len(status)]
            }

            print(f'Creating batch {i+1} for development {dev["id"]}...')

            batch_id = colina_db.insert(table='batches', data=batch_data)

            batch_assets_data = {
                'batch_id': batch_id,
                'asset_url': 'public/colina.png'
            }

            colina_db.insert(table='batch_assets', data=batch_assets_data)

            batch_payment_plans_data = {
                'batch_id': batch_id,
                'payment_plan_id': payment_plan_id
            }

            colina_db.insert(table='batch_payment_plans', data=batch_payment_plans_data)

print('Creating developments...')
create_devs(50)
print('Developments created')

print('Creating batches...')
create_batches(100)
print('Batches created')