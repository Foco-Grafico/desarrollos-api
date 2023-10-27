from services.db import colina_db
from app.models.development import CreateDevelopment
from fastapi import Depends, HTTPException
from app.utils import auth, perms
from app.enums.permissions import DEVELOPMENT
from app.utils.files import save_file_on_api, is_image

def dev(token: str, dev: CreateDevelopment = Depends(CreateDevelopment.as_form)):
    perm = perms.get_perm_id(DEVELOPMENT.CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')



    if not is_image(dev.logo):
        raise HTTPException(
            status_code=400,
            detail='The logo must be an image.'
        )

    logo_url = save_file_on_api(
        file=dev.logo,
        path='public/devs'
    )

    try:
        colina_db.insert(
            table='developments',
            data={
                'name': dev.name,
                'description': dev.description,
                'address': dev.address,
                'city': dev.city,
                'state': dev.state,
                'country': dev.country,
                'logo_url': logo_url,
                'contact_number': dev.contact_number,
                'contact_email': dev.contact_email
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, 
            detail='An error occurred while creating the development.'
        )

    return {
        'message': 'Development created successfully.'
    }