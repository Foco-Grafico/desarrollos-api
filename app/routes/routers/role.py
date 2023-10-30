from fastapi import APIRouter
from app.routes.controllers.roles import create, add_perm

router = APIRouter(prefix='/role', tags=['role'])

router.post('')(create.role)
router.post('/add-perm')(add_perm.add_new_permssion_to_role)