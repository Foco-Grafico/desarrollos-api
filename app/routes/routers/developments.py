from fastapi import APIRouter
from app.routes.controllers.development import create, delete, get, modify, assign



router = APIRouter(
    prefix='/development',
    tags=['development']
)

router.post('')(create.dev)
router.delete("")(delete.delete_dev)
router.get('')(get.get_devs)
router.get('/{development_id}')(get.get_dev)
router.put('/{development_id}')(modify.modify_dev)
router.post('/{development_id}/assign/{seller_id}')(assign.assign_seller)
router.delete('/{development_id}/unassign/{seller_id}')(assign.unassign_seller)
