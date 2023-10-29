from fastapi import APIRouter
from app.routes.controllers.sellers import create

router = APIRouter(prefix='/seller', tags=['seller'])

router.post('')(create.seller)