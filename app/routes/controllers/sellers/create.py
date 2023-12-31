from services.db import colina_db
from fastapi import HTTPException, Depends
from app.enums.permissions import SELLER
from app.models.seller import CreateSeller
from app.utils import auth, perms

async def seller(token: str, seller: CreateSeller = Depends(CreateSeller.as_form)):
    perm = perms.get_perm_id(SELLER.CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')
    
    try:
        seller_id = colina_db.insert(
            table='sellers',
            data={
                'name': seller.first_name,
                'last_name': seller.last_name,
                'email': seller.email,
                'phone': seller.phone_number,
                'enterprise': seller.enterprise,
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while creating the seller.')
    
    return {
        'seller_id': seller_id,
        'status': 'success',
        'message': 'Seller created successfully.',
    }

