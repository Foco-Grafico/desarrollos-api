from app.models.batch import CreateBatch
from fastapi import Depends, HTTPException
from services.db import colina_db
from app.utils.perms import is_have_perm
from app.enums.permissions import BATCH

async def batch(token: str, batch: CreateBatch = Depends(CreateBatch.as_form)):
    if not is_have_perm(token, BATCH.CREATE.value):
        raise HTTPException(status_code=403, detail="You don't have permission to create batches")

    dev_db = colina_db.fetch_one(
        sql='SELECT * FROM developments WHERE id = %s',
        params=(batch.development_id,)
    )

    if not dev_db:
        raise HTTPException(status_code=404, detail="Development not found")

    try:
        colina_db.insert(
            table='batches',
            data={
                'area': batch.area,
                'price': batch.price,
                'perimeter': batch.perimeter,
                'longitude': batch.longitude,
                'coords': batch.coords,
                'amenities': batch.amenities,
                'development_id': batch.development_id
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while creating batch")
    
    return {
        'message': 'Batch created successfully'
    }