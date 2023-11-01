from fastapi import APIRouter
from app.routes.controllers.development import create, delete


router = APIRouter(
    prefix='/development',
    tags=['development']
)

router.post('')(create.dev)
router.delete("")(delete.delete_dev)
