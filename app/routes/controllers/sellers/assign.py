from fastapi import HTTPException
from services.db import colina_db

async def assign_seller_to_dev(seller_id: int, dev_id: int):
    seller = colina_db.select_one(
        table='sellers',
        columns=['*'],
        where={
            'id': seller_id
        }
    )

    if not seller:
        raise HTTPException(status_code=404, detail='Seller not found')
    
    dev = colina_db.select_one(
        table='developments',
        columns=['*'],
        where={
            'id': dev_id
        }
    )

    if not dev:
        raise HTTPException(status_code=404, detail='Development not found')
    
