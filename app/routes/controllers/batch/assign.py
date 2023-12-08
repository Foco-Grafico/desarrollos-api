from fastapi import HTTPException, Body
from services.db import colina_db
from typing import Annotated
from app.utils.perms import is_have_perm
from app.enums.permissions import BATCH
from random import randint
from services.whatsapp.controller.send import send_controller as send_whatsapp
from services.whatsapp.models.wa_models import Buttons, Button
from app.utils.intervals import setInterval

async def assign_batch_random_seller(token: str, batch_id: int, dev_id: int, client_phone: str, client_name: str, mail: str):
    if not is_have_perm(token, BATCH.MODIFY.value):
        raise HTTPException(status_code=403, detail="You don't have permission to create batches")
    
    sellers = colina_db.fetch_all(
        sql='SELECT * FROM sellers WHERE id IN (SELECT seller_id FROM developments_sellers WHERE development_id = %s)',
        params=(dev_id,)
    )

    if not sellers:
        raise HTTPException(status_code=404, detail="No sellers found for this development")

    get_random_seller = lambda: sellers[randint(0, len(sellers) - 1)]

    send_seller_message = lambda seller_phone: send_whatsapp(
        to=seller_phone,
        message=Buttons(
            body='Hola, te presento a un nuevo cliente potencial',
            buttons=[
                Button(
                    execute=f'accept_seller batch"{batch_id}" client_p"{client_phone}" client_n"{client_name}"',
                    title='Aceptar'
                )
            ],
            footer='Tienes 5 min para aceptar.'
        )
    )

    random_seller = get_random_seller()
    send_seller_message(random_seller['phone'])

    try:
        colina_db.insert(
            table='batch_sellers',
            data={
                'batch_id': batch_id,
                'seller_id': random_seller['id'],
                'status': 'pending',
                'client_phone': client_phone,
                'client_name': client_name,
                'client_mail': mail
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while saving this seller")

    def action(inter: setInterval):
        batch_seller = colina_db.fetch_one(
            sql='SELECT status FROM batch_sellers WHERE batch_id = %s AND client_phone = %s',
            params=(batch_id, client_phone)
        )

        if batch_seller['status'] == 'pending':
            new_random_seller = get_random_seller()
            
            while new_random_seller['id'] == random_seller['id']:
                new_random_seller = get_random_seller()

            send_seller_message(new_random_seller['phone'])
            colina_db.update(
                table='batch_sellers',
                data={
                    'seller_id': new_random_seller['id']
                },
                where=f'batch_id = {batch_id} AND client_phone = {client_phone}'
            )
        else:
            inter.cancel()

    setInterval(
        interval=20,
        action=action
    )

    return {
        'message': 'Seller assigned successfully'
    }


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