from fastapi import APIRouter
from app.routes.controllers.sellers import create, modify, delete, get

router = APIRouter(prefix='/seller', tags=['seller'])

router.post('')(create.seller)
router.put('/{seller_id}')(modify.modify_seller)
router.delete('/{seller_id}')(delete.delete_seller)
router.get('')(get.get_sellers)
router.get('/{dev}')(get.get_sellers_in_dev)