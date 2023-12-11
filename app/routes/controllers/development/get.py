from fastapi import HTTPException
from pytest import param
from services.db import colina_db

async def get_devs():
    devs = colina_db.fetch_all(
        sql="SELECT d.*, UUID() as `key` FROM developments d",
    )
    
    return {
        'message': 'Developments found successfully.',
        'data': devs
    }

async def get_dev(development_id: int | str):
    dev = colina_db.fetch_one(
        sql = "SELECT d.*, UUID() as `key` FROM developments d WHERE id = %s",
        params=(development_id,)
    )

    if not dev:
        dev = colina_db.select_one(
            table='developments d',
            columns=['d.*, UUID() as `key`'],
            where={
                'slug': development_id
            }
        )

    if not dev:
        raise HTTPException(status_code=404, detail="Development not found")
    
    sqm_list = colina_db.fetch_all(
        sql="SELECT DISTINCT sq_m FROM batches WHERE development_id = %s",
        params=(dev['id'],)
    )

    price_range = colina_db.fetch_one(
        sql="SELECT MIN(price) as min, MAX(price) as max FROM batches WHERE development_id = %s",
        params=(dev['id'],)
    )

    return {
        "message": 'Development found successfully.',
        "data": dev,
        "sqm_list": list(map(
            lambda sqm: sqm['sq_m'],
            sqm_list
        )),
        "price_range": price_range
    }
 