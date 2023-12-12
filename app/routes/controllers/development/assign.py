from services.db import colina_db
from fastapi import HTTPException

async def assign_seller(seller_id: int, development_id: int):
    try:
        colina_db.insert(
            table='developments_sellers',
            data={
                'development_id': development_id,
                'seller_id': seller_id,
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while assigning the seller to the developer.')
    
    return {
        'status': 'success',
        'message': 'Seller assigned successfully.',
    }

async def unassign_seller(seller_id: int, development_id: int):
    try:
        colina_db.execute(
            sql='DELETE FROM developments_sellers WHERE development_id = %s AND seller_id = %s',
            params=(development_id, seller_id),
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while unassigning the seller from the developer.')
    
    return {
        'status': 'success',
        'message': 'Seller unassigned successfully.',
    }