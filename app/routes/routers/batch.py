from fastapi import APIRouter
from app.routes.controllers.batch import create, delete

router = APIRouter(
    prefix='/batch',
    tags=['batch']
)

router.post('')(create.batch)
router.delete('')(delete.batch)

