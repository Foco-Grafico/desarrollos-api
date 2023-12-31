from mysqlclientpy import DB
from dotenv import load_dotenv
import os
import math
import random
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

seller_data = [
    {
        'name': 'Enrique',
        'last_name': 'De alba',
        'email': 'jedealbagaytan@gmail.com',
        'phone': '5216693171220',
        'enterprise': 'Deluxe'
    },
    {
        'name': 'Hugo',
        'last_name': 'Gei',
        'email': 'aaaaaaa',
        'phone': '5216691006732',
        'enterprise': 'Deluxe'
    }
]

colina_db.insert_many(table='sellers', data=seller_data)

def create_devs(num_devs: int):
    sellers = colina_db.select(table='sellers', columns=['id'])
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
            'contact_email': 'contact@colina.com',
            'max_blocks': 2,
            'view_url': "https://www.klapty.com/tour/tunnel/Ua30Cj4PJb" if i % 2 == 0 else None,
            'slug': f'desarrollo-{i+1}'
        }
        print(f'Creating development {i+1}...')

        id = colina_db.insert(table='developments', data=dev_data)

        for seller in sellers:
            colina_db.insert(table='developments_sellers', data={
                'development_id': id,
                'seller_id': seller['id']
            })

def create_batches(num_batch_per_dev: int):
    devs = colina_db.select(table='developments', columns=['id'])

    # currecies = ['MXN', 'USD', 'EUR', 'CAD', 'GBP', 'JPY', 'CNY', 'CHF', 'AUD', 'NZD']
    status = [1, 2, 3]

    for dev in devs:
        for i in range(num_batch_per_dev):
            payment_plan = {
                'months_to_pay': 6,
                'interest_rate': 0.1,
                'annuity': i+1*math.pi,
                'pay_per_month': (100000+(100000*0.1))/6,
                'payment_method': 'payment_method',
                'price': 100000,
                'down_payment': 10000
            }

            print(f'Creating payment plan {i+1} for development {dev["id"]}...')

            payment_plan_id = colina_db.insert(table='payment_plans', data=payment_plan)

            batch_data = {
                'area': 100,
                'price': random.randint(30000, 1000000),
                'perimeter': 100,
                'longitude': 100,
                'coords': 'coords',
                'development_id': dev['id'],
                'currency': 'MXN',
                'location': 'location',
                'sq_m': random.randint(1, num_batch_per_dev),
                'amenities': 'amenities',
                'sides': 4,
                'block': 1 if i % 2 == 0 else 2,
                'number_of_batch': i+1,
                'status': status[i % len(status)],
                'type': i % 7 + 1
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
create_batches(750)
print('Batches created')