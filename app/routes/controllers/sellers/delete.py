from email import message
from math import e
from fastapi import HTTPException
from app.routes.controllers.sellers.create import seller
from app.utils import perms, auth
from app.enums.permissions import SELLER
from services.db import colina_db

async def delete_seller(token: str, seller_id: int):
    perm = perms.get_perm_id(SELLER.DELETE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')
    
    seller = colina_db.fetch_one(
        sql="SELECT id FROM sellers WHERE id = %s",
        params=(seller_id,)
    )

    if not seller:
        raise HTTPException(status_code=404, detail='Seller not found.')
    
    try:
        colina_db.execute(
            sql="DELETE FROM sellers WHERE id = %s",
            params=(seller_id,)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while deleting the seller.')

    return {
        "message": "Seller deleted"
    }
    