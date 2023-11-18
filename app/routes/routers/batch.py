from fastapi import APIRouter
from app.routes.controllers.batch import create, delete, assign, modify, get

router = APIRouter(
    prefix='/batch',
    tags=['batch']
)

router.post('')(create.batch)
router.delete('')(delete.batch)
router.post('/assign/asset')(assign.assign_batch_asset)
router.post('/assign/payment-plan')(assign.assign_batch_payment_plan)
router.put('/{batch_id}')(modify.modify_batch)
router.put('/asset/{asset_id}')(modify.modify_batch_asset)
router.delete('/asset/{asset_id}')(delete.delete_image_from_batch)
router.get('')(get.get_batches)
router.post('/{development_id}')(get.get_batch_in_dev)
router.get('/types')(get.get_batches_types)
router.get('/{development_id}/{batch_id}')(get.get_batch_in_dev_by_id)

