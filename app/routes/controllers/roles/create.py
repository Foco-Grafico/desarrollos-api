from services.db import colina_db
from fastapi import HTTPException
from app.enums.permissions import ROLE
from app.models.role import CreateRole
from app.utils import auth, perms

async def role(token: str, role: CreateRole):
    perm = perms.get_perm_id(ROLE.CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    try:
        role_id = colina_db.insert(
            table='roles',
            data={
                'name': role.name,
                'description': role.description
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='An error occurred while creating the account.')

    for perm_id in role.permissions:
        try:
            colina_db.insert(
                table='rol_perms',
                data={
                    'role_id': role_id,
                    'perm_id': perm_id
                }
            )
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='An error occurred while adding the role permission.')


    return {
        'status': 'success',
        'message': 'Role created successfully.'
    }