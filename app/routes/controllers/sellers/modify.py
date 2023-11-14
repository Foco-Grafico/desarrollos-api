from services.db import colina_db
from fastapi import HTTPException, Depends
from app.utils import auth, perms
from app.enums.permissions import SELLER
from app.models.seller import EditSeller

async def modify_seller(
    token: str,
    seller_id: int,
    seller: EditSeller = Depends(EditSeller.as_form),
):
    perm = perms.get_perm_id(SELLER.UPDATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    seller_db = colina_db.fetch_one(
        sql= "SELECT * FROM sellers WHERE id = %s",
        params=(seller_id,)
    )


    if not seller_db:
        raise HTTPException(status_code=404, detail="Seller not found")


    try:
        colina_db.update(
            table= 'sellers',
            where= f'id = {seller_id}',
            data= {
                'name': seller.first_name if seller.first_name is not None else seller_db['first_name'],
                'last_name': seller.last_name if seller.last_name is not None else seller_db['last_name'],
                'email': seller.email if seller.email is not None else seller_db['email'],
                'phone': seller.phone_number if seller.phone_number is not None else seller_db['phone_number'],
                'enterprise': seller.enterprise if seller.enterprise is not None else seller_db['enterprise'],
            },

        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail= 'Development could not be updated')
    
    return {
        'message': 'Seller updated successfully'
    }