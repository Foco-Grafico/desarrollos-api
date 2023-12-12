from services.db import colina_db

async def get_sellers():
    sellers = colina_db.select(
        table='sellers',
        columns=['*', 'UUID() as `key`']
    )

    return {
        'message': 'Sellers found',
        'data': sellers
    }

async def get_sellers_in_dev(dev: int):
    sellers = colina_db.fetch_all(
        'SELECT s.*, UUID() as `key` FROM sellers s WHERE id IN (SELECT seller_id FROM developments_sellers WHERE development_id = %s)',
        (dev,)
    )

    return {
        'message': 'Sellers found',
        'data': sellers
    }