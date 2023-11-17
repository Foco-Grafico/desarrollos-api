from fastapi import HTTPException
from pytest import param
from services.db import colina_db

async def get_devs():
    devs = colina_db.fetch_all(
        sql="SELECT d.*, UUID() as `key` FROM developments d",
    )

    if not devs:
        raise HTTPException(status_code=404, detail="No developments found")
    
    return {
        'message': 'Developments found successfully.',
        'data': devs
    }

async def get_dev(development_id: int):
    dev = colina_db.fetch_one(
        sql = "SELECT * FROM developments WHERE id = %s",
        params=(development_id,)
    )

    if not dev:
        raise HTTPException(status_code=404, detail="Development not found")
    
    return {
        "message": 'Development found successfully.',
        "data": dev
    }
 