from services.db import colina_db
from fastapi import HTTPException, Depends
from app.utils import auth, perms
from app.enums.permissions import DEVELOPMENT
from app.models.development import EditDevelopment
from app.utils.files import save_file_on_api, is_image

async def modify_dev(
    token: str,
    development_id: int,
    dev: EditDevelopment = Depends(EditDevelopment.as_form)
):
    perm = perms.get_perm_id(DEVELOPMENT.MODIFY.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail='You do not have permission to perform this action.')

    development_db = colina_db.fetch_one(
        sql= "SELECT * FROM developments WHERE id = %s",
        params=(development_id,)
    )


    if not development_db:
        raise HTTPException(status_code=404, detail="Development not found")


    logo_url = development_db['logo_url']
    if dev.logo is not None:
        if not is_image(dev.logo):
            raise HTTPException(status_code=400, detail="Logo must be an image")

        logo_url = save_file_on_api(
            file=dev.logo,
            path=development_db['logo_url'],
            exact_path=True
        )

    try:
        colina_db.update(
            table= 'developments',
            where= f'id = {development_id}',
            data= {
                'name': dev.name if dev.name is not None else development_db['name'],
                'description': dev.description if dev.description is not None else development_db['description'],
                'address': dev.address if dev.address is not None else development_db['address'],
                'city': dev.city if dev.city is not None else development_db['city'],
                'state': dev.state if dev.state is not None else development_db['state'],
                'country': dev.country if dev.country is not None else development_db['country'],
                'logo_url': logo_url,
                'contact_number': dev.contact_number if dev.contact_number is not None else development_db['contact_number'],
                'contact_email': dev.contact_email if dev.contact_email is not None else development_db['contact_email']
            },

        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Development could not be updated')

    return {
        'message': 'Development updated successfully.'
    }