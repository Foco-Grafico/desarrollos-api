from fastapi import HTTPException, Body
from services.db import colina_db
from typing import Annotated
from app.utils.perms import is_have_perm
from app.enums.permissions import BATCH

async def assign_batch_asset(token: str, asset_url: Annotated[str, Body(..., embed=True)], batch_id: int):
    if not is_have_perm(token, BATCH.MODIFY.value):
        raise HTTPException(status_code=403, detail="You don't have permission to create batches")
    try:
        colina_db.insert(
            table='batch_assets',
            data={
                'asset_url': asset_url,
                'batch_id': batch_id
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while saving this asset")

    return {
        'message': 'Asset created successfully'
    }

async def assign_batch_payment_plan(token: str, batch_id: int, plan_id: int):
    if not is_have_perm(token, BATCH.MODIFY.value):
        raise HTTPException(status_code=403, detail="You don't have permission to create batches")
    
    try:
        colina_db.insert(
            table='batch_payment_plans',
            data={
                'batch_id': batch_id,
                'payment_plan_id': plan_id
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while saving this payment plan")

    return {
        'message': 'Payment plan assigned successfully'
    }