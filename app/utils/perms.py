from services.db import colina_db

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