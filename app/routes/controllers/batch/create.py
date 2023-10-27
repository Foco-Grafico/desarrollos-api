from app.models.batch import CreateBatch
from fastapi import Depends

async def batch(batch: CreateBatch = Depends(CreateBatch.as_form)):
    pass