from fastapi import APIRouter
from app.routes.controllers.sellers import create, modify, delete

router = APIRouter(prefix='/seller', tags=['seller'])

router.post('')(create.seller)
router.put('/{seller_id}')(modify.modify_seller)
router.delete('')(delete.delete_seller)