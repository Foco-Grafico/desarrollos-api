from app.models.account import AccountCreate
from fastapi import HTTPException
from app.utils import auth, perms
from app.enums.permissions import ACCOUNT
from services.db import colina_db
import bcrypt
import uuid

async def account(token: str, account: AccountCreate):
    perm = perms.get_perm_id(ACCOUNT.CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    try:
        colina_db.insert(
            table='users',
            data={
                'name': account.name,
                'email': account.email,
                'token': bcrypt.hashpw(account.password.encode('utf-8'), bcrypt.gensalt())
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while creating the account.')
    
    """
    user = colina_db.fetch_one(
        params=(account.email,),
        sql=  SELECT BIN_TO_UUID(id) as id FROM users WHERE email = %s
    )
    """

    
    user = colina_db.select_one(
        table='users',
        columns=['BIN_TO_UUID(id) as id'],
        where={
            'email': account.email
        }
    )
    


    return {
        'status': 'success',
        'message': 'Account created successfully.',
        "id": user['id']
    }