from services.db import colina_db
from fastapi import HTTPException
from app.utils import auth, perms, files
from app.enums.permissions import BATCH

async def batch(token: str, id: int):
    perm = perms.get_perm_id(BATCH.DELETE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    batch_db = colina_db.fetch_one(
        sql="SELECT id FROM batches WHERE id = %s",
        params=(id,)
    )

    if not batch_db:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    batch_files = colina_db.fetch_all(
        sql="SELECT * FROM batch_assets WHERE batch_id = %s",
        params=(id,)
    )

    try:
        colina_db.execute(
            sql="DELETE FROM batches WHERE id = %s",
            params=(id,)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while deleting the batch.')

    for file_content in batch_files:
        files.delete_file(file_content['asset_url'])

    return {
        "message": "Batch deleted"
    }

async def delete_image_from_batch(asset_id: int):
    asset_db = colina_db.fetch_one(
        sql="SELECT * FROM batch_assets WHERE id = %s",
        params=(asset_id,)
    )

    if not asset_db:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    try:
        colina_db.execute(
            sql="DELETE FROM batch_assets WHERE id = %s",
            params=(asset_id,)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while deleting the asset.')

    files.delete_file(asset_db['asset_url'])

    return {
        "message": "Asset deleted"
    }