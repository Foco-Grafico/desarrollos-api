from fastapi import HTTPException
from services.db import colina_db

async def get_batches():
    batches = colina_db.fetch_all(
        sql="SELECT * FROM batches"
    )

    if not batches:
        raise HTTPException(
            status_code=404,
            detail="No batches found"
        )

    for batch in batches:
        batch['assets'] = colina_db.fetch_all(
            sql="SELECT * FROM batch_assets WHERE batch_id = %s",
            params=(batch['id'],)
        )

        batch['payment_plans'] = colina_db.fetch_all(
            sql="SELECT * FROM batch_payment_plans WHERE batch_id = %s",
            params=(batch['id'],)
        )

    return {
        'message': 'Batches found',
        'data': batches
    }

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

    batch['assets'] = colina_db.fetch_all(
            sql="SELECT * FROM batch_assets WHERE batch_id = %s",
            params=(batch['id'],)
        )

    batch['payment_plans'] = colina_db.fetch_all(
        sql="SELECT * FROM batch_payment_plans WHERE batch_id = %s",
        params=(batch['id'],)
    )
        
    return {
        'message': 'Batch found successfully',
        'data': batch_db
    }
