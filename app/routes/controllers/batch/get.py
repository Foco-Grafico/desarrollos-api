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