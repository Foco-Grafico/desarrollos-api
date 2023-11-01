from app.routes.controllers.batch.create import batch
from services.db import colina_db
from app.models.development import CreateDevelopment
from fastapi import Depends, HTTPException
from app.utils import auth, perms, files
from app.enums.permissions import DEVELOPMENT



async def delete_dev(token: str,development_id: int):
    perm = perms.get_perm_id(DEVELOPMENT.DELETE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')
    
    development_db = colina_db.fetch_one(
        sql= "SELECT * FROM developments WHERE id = %s",
        params=(development_id,)
    )

    if not development_db:
        raise HTTPException(status_code=404, detail="Development not found")

    try: 
        colina_db.execute(
            sql="DELETE FROM developments WHERE id = %s",
            params=(development_id,),
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Development could not be deleted')
    
    files.delete_file(development_db['logo_url'])    

    return {
        'message': 'Development deleted successfully.'
    }