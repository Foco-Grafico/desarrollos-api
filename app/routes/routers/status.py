from fastapi import APIRouter
from app.routes.controllers.status import get

router = APIRouter(
    prefix='/status',
    tags=['status']
)

router.get('/batch')(get.get_batch_statuses)
router.get('/dev')(get.get_devs_status)