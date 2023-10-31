from fastapi import APIRouter
from app.routes.controllers.development import create

router = APIRouter(
    prefix='/development',
    tags=['development']
)

router.post('')(create.dev)
