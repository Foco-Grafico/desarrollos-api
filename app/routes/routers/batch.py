from fastapi import APIRouter
from app.routes.controllers.batch import create, delete, assign, modify

router = APIRouter(
    prefix='/batch',
    tags=['batch']
)

router.post('')(create.batch)
router.delete('')(delete.batch)
router.post('/assign/asset')(assign.assign_batch_asset)
router.post('/assign/payment-plan')(assign.assign_batch_payment_plan)
router.put('/{batch_id}')(modify.modify_batch)

