from services.db import colina_db
from fastapi import HTTPException
from app.enums.permissions import ROLE
from app.utils import auth, perms

async def add_new_permssion_to_role(token: str, role_id: int, perm_str: str):
    perm = perms.get_perm_id(ROLE.UPDATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    try:
        perm_id = perms.get_perm_id(perm_str)

        colina_db.insert(
            data={
                'role_id': role_id,
                'perm_id': perm_id
            },
            table='rol_perms'
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error while inserting rol perm in role: {role_id}.')

    return {
        'message': f'Permission {perm_str} added to role {role_id}.'
    }