from services.db import colina_db

async def get_batch_statuses():
    batch_statuses = colina_db.select(
        table='batch_status',
        columns=['*', 'UUID() as `key`']
    )

    return {
        'message': 'Batch statuses found',
        'data': batch_statuses
    }

async def get_devs_status():
    dev_statuses = colina_db.select(
        table='dev_status',
        columns=['*', 'UUID() as `key`']
    )

    return {
        'message': 'Development statuses found',
        'data': dev_statuses
    }