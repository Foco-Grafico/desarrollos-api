from fastapi import HTTPException, Body
from services.db import colina_db
from typing import Annotated

async def assign_batch_asset(asset_url: Annotated[str, Body(..., embed=True)], batch_id: int):
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

async def assign_batch_payment_plan(batch_id: int, plan_id: int):
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