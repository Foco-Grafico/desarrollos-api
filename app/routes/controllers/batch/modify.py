from services.db import colina_db
from fastapi import HTTPException, Depends, UploadFile
from app.utils import auth, perms, files
from app.enums.permissions import BATCH
from app.models.batch import EditBatch
from app.enums.statuses import STATUS_BATCH

async def modify_batch_asset(token: str, asset_id: int, file: UploadFile):
    perm = perms.get_perm_id(BATCH.MODIFY.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    file_db = colina_db.fetch_one(
        sql='SELECT * FROM batch_assets WHERE id = %s',
        params=(asset_id,)
    )

    if not file_db:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    if not files.is_image(file):
        raise HTTPException(status_code=400, detail="Asset must be an image")
    
    image_url = files.save_file_on_api(
        file=file,
        path=file_db['asset_url'],
        exact_path=True
    )

    try:
        colina_db.update(
            table='batch_assets',
            where=f'id = "{asset_id}"',
            data={
                'asset_url': image_url
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while updating this asset")
    
    return {
        'message': 'Asset updated successfully'
    }

async def modify_batch(
    token: str,
    batch_id: int,
    status: STATUS_BATCH | None = None,
    batch: EditBatch = Depends(EditBatch.as_form)
):
    perm = perms.get_perm_id(BATCH.MODIFY.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    batch_db = colina_db.fetch_one(
        sql= "SELECT * FROM batches WHERE id = %s",
        params=(batch_id,)
    )
    if not batch_db:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    try:
        colina_db.update(
            table= 'batches',
            where= f'id = {batch_id}',
            data= {
                'area': batch.area if batch.area is not None else batch_db['area'],
                'perimeter': batch.perimeter if batch.perimeter is not None else batch_db['perimeter'],
                'longitude': batch.longitude if batch.longitude is not None else batch_db['longitude'],
                'coords': batch.coords if batch.coords is not None else batch_db['coords'],
                'amenities': batch.amenities if batch.amenities is not None else batch_db['amenities'],
                'price': batch.price if batch.price is not None else batch_db['price'],
                'development_id': batch.development_id if batch.development_id is not None else batch_db['development_id'],
                'status': status.value if status is not None else batch_db['status'],
                'currency': batch.currency if batch.currency is not None else batch_db['currency'],
                'location': batch.location if batch.location is not None else batch_db['location'],
                'sq_m': batch.sq_m if batch.sq_m is not None else batch_db['sq_m'],
                'sides': batch.sides if batch.sides is not None else batch_db['sides'],
                'block': batch.block if batch.block is not None else batch_db['block'],
                'number_of_batch': batch.number_of_batch if batch.number_of_batch is not None else batch_db['number_of_batch'],
                'type': batch.type if batch.type is not None else batch_db['type']
            },
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Batch could not be updated')
    return {
        'message': 'Batch updated successfully.'
    }