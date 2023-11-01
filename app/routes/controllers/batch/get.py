from fastapi import HTTPException
from services.db import colina_db


async def get_batch_in_dev(development_id:int,):
    batch_db = colina_db.fetch_all(
        sql="SELECT * FROM batches WHERE development_id = %s",
        params=(development_id,)
    )

    if not batch_db:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    return batch_db

    
    