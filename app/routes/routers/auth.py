from fastapi import APIRouter
from app.routes.controllers.auth import create

router = APIRouter(prefix='/auth', tags=['auth'])

router.post('/account')(create.account)