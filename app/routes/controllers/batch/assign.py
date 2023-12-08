from fastapi import HTTPException, Body
from services.db import colina_db
from typing import Annotated
from app.utils.perms import is_have_perm
from app.enums.permissions import BATCH
from random import randint
from services.whatsapp.controller.send import send_controller as send_whatsapp
from services.whatsapp.models.wa_models import Buttons, Button

async def assign_batch_random_seller(token: str, batch_id: int, dev_id: int, client_phone: str):
    if not is_have_perm(token, BATCH.MODIFY.value):
        raise HTTPException(status_code=403, detail="You don't have permission to create batches")
    
    sellers = colina_db.fetch_all(
        sql='SELECT * FROM sellers WHERE id IN (SELECT seller_id FROM developments_sellers WHERE development_id = %s)',
        params=(dev_id,)
    )

    if not sellers:
        raise HTTPException(status_code=404, detail="No sellers found for this development")

    random_seller = sellers[randint(0, len(sellers) - 1)]

    send_whatsapp(
        to=random_seller['phone'],
        message=Buttons(
            body='Hola, te presento a un nuevo cliente potencial',
            buttons=[
                Button(
                    execute=f'accept_seller batch"{batch_id}" client"{client_phone}"',
                    title='Aceptar'
                ),
                Button(
                    execute=f'reject_seller batch"{batch_id}" client"{client_phone}"',
                    title='Rechazar'
                )
            ],
            footer='Si no aceptas en los próximos 5 minutos, el cliente será asignado a otro vendedor'
        )
    )

    pass

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