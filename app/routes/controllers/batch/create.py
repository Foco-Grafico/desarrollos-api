from app.models.batch import CreateBatch
from fastapi import Depends, HTTPException
from services.db import colina_db
from app.utils.perms import is_have_perm
from app.enums.permissions import BATCH
from app.utils.files import save_file_on_api, is_image
from app.routes.controllers.batch.assign import assign_batch_asset
from app.enums.statuses import STATUS_BATCH

async def batch(token: str, status: STATUS_BATCH | None = None, batch: CreateBatch = Depends(CreateBatch.as_form)):
    if not is_have_perm(token, BATCH.CREATE.value):
        raise HTTPException(status_code=403, detail="You don't have permission to create batches")

    dev_db = colina_db.fetch_one(
        sql='SELECT * FROM developments WHERE id = %s',
        params=(batch.development_id,)
    )

    if not dev_db:
        raise HTTPException(status_code=404, detail="Development not found")

    try:
        batch_id = colina_db.insert(
            table='batches',
            data={
                'area': batch.area,
                'price': batch.price,
                'perimeter': batch.perimeter,
                'longitude': batch.longitude,
                'coords': batch.coords,
                'amenities': batch.amenities,
                'development_id': batch.development_id,
                'currency': batch.currency,
                'location': batch.location,
                'sq_m': batch.sq_m,
                'status': status.value if status is not None else STATUS_BATCH.AVAILABLE.value
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while creating batch")
    
    assets_log = {}

    for file in batch.assets:
        if not is_image(file):
            raise HTTPException(status_code=400, detail="Assets must be images")
        
        file_url = save_file_on_api(
            file=file,
            path='public/batches'
        )

        try:
            await assign_batch_asset(
                token=token,
                asset_url=file_url,
                batch_id=batch_id
            )

            assets_log[file.filename] = 'Asset created successfully'
        except Exception as e:
            print(e)
            assets_log[file.filename] = 'An error occurred while saving this asset'

    return {
        'batch_id': batch_id,
        'message': 'Batch created successfully',
        'assets_log': assets_log
    }