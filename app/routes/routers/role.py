from fastapi import APIRouter
from app.routes.controllers.roles import create

router = APIRouter(prefix='/role', tags=['role'])

router.post('')(create.role)