from fastapi import APIRouter
from app.routes.controllers.auth import create, add_perm

router = APIRouter(prefix='/auth', tags=['auth'])

router.post('/account')(create.account)
router.post('/add-perm')(add_perm.add_new_permssion_to_user)
