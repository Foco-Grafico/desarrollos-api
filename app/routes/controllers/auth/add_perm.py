from services.db import colina_db
from fastapi import HTTPException
from app.enums.permissions import ACCOUNT
from app.utils import auth, perms

async def add_new_permssion_to_user(token: str, user_id: str, perm_str: str):
    perm = perms.get_perm_id(ACCOUNT.ADD_PERMISSION.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    try:
        perm_id = perms.get_perm_id(perm_str)

        colina_db.insert(
            data={
                'user_id': f'UUID_TO_BIN({user_id})',
                'perm_id': perm_id
            },
            table='user_perms'
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error while inserting perm in user: {user_id}.')

    return {
        'message': f'Permission {perm_str} added to user {user_id}.'
    }
