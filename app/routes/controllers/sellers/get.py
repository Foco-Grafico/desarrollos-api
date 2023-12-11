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