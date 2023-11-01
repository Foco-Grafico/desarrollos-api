from services.db import colina_db
from app.utils.auth import verify_perm

def get_perm_id(name: str) -> int:
    perm = colina_db.fetch_one(
        sql='SELECT id FROM permissions WHERE name = LOWER(%s);',
        params=(name,)
    )

    if perm:
        id = perm['id']
    else:
        id = colina_db.insert(
            data={
                'name': name.lower()
            },
            table='permissions',
        )

    return id

def is_have_perm(token: str, perm: str):
    perm_id = get_perm_id(perm)

    if not verify_perm(token, perm_id):
        return False
    
    return True