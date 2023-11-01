from fastapi import APIRouter
from app.routes.controllers.sellers import create, delete

router = APIRouter(prefix='/seller', tags=['seller'])

router.post('')(create.seller)
router.delete('')(delete.delete_seller)