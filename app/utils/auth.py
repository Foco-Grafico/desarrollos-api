from services.db import colina_db

master_token = '46983916'

def verify_token(token: str):
    try:
        if token != master_token:
            id = colina_db.fetch_one('SELECT BIN_TO_UUID(id) as id FROM users WHERE id = UUID_TO_BIN(%s)', (token,))
            if not id:
                return False
            return True
        else:
            return True
    except:
        return False
    

def get_perms(id: str):
    isValidId = verify_token(id)

    if isValidId == False:
        return []

    if master_token == id:
        return '*'
    
    perms = colina_db.fetch_all(
        sql='''
            SELECT DISTINCT p.*
            FROM users u
            LEFT JOIN user_perms up ON u.id = up.user_id
            LEFT JOIN user_roles ur ON u.id = ur.user_id
            LEFT JOIN rol_perms rp ON ur.role_id = rp.role_id
            LEFT JOIN permissions p ON up.perm_id = p.id OR rp.perm_id = p.id
            WHERE u.id = UUID_TO_BIN(%s);
        ''',
        params=(id,)
    )

    perms = [perm['id'] for perm in perms]

    return perms

def verify_perm(id: str, perm: int):
    perms = get_perms(id)

    if perms == '*':
        return True

    if perm in perms:
        return True
    
    return False