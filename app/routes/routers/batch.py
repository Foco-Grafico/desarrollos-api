from fastapi import APIRouter
from app.routes.controllers.batch import create, delete, assign, get

router = APIRouter(
    prefix='/batch',
    tags=['batch']
)

router.post('')(create.batch)
router.delete('')(delete.batch)
router.post('/assign/asset')(assign.assign_batch_asset)
router.post('/assign/payment-plan')(assign.assign_batch_payment_plan)
router.get('')(get.get_batch_in_dev)

