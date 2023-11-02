from services.db import colina_db
from fastapi import HTTPException, Depends
from app.utils import auth, perms
from app.enums.permissions import BATCH
from app.models.batch import EditBatch

async def modify_batch(
    token: str,
    batch_id: int,
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
        batch_data = colina_db.update(
            table= 'batches',
            where= f'id = {batch_id}',
            data= {
                'area': batch.area if batch.area is not None else batch_db['area'],
                'perimeter': batch.perimeter if batch.perimeter is not None else batch_db['perimeter'],
                'longitude': batch.longitude if batch.longitude is not None else batch_db['longitude'],
                'coords': batch.coords if batch.coords is not None else batch_db['coords'],
                'amenities': batch.amenities if batch.amenities is not None else batch_db['amenities'],
                'price': batch.price if batch.price is not None else batch_db['price'],
                'assets': batch.assets if batch.assets is not None else batch_db['assets'],
                'development_id': batch.development_id if batch.development_id is not None else batch_db['development_id']
            },
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Batch could not be updated')
    return {
        'message': 'Batch updated successfully.',
        "data": batch_data
    }