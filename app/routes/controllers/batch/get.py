from fastapi import HTTPException
from services.db import colina_db


async def get_batch_in_dev(development_id:int,):
    dev_db = colina_db.fetch_one(
        sql="SELECT id FROM developments WHERE id = %s",
        params=(development_id,)
    )

    if not dev_db:
        raise HTTPException(status_code=404, detail="Development not found")

    batch_db = colina_db.fetch_all(
        sql="SELECT * FROM batches WHERE development_id = %s",
        params=(development_id,)
    )

    if not batch_db:
        raise HTTPException(status_code=404, detail="Batch not found")

    return {
        'message': 'Batch found successfully',
        'data': batch_db
    }
