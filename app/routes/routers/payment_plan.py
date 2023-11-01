from fastapi import APIRouter
from app.routes.controllers.payment_plan import create

router = APIRouter(
    prefix='/payment',
    tags=['payment_plan']
)

router.post('')(create.payment_plan)

