from fastapi import APIRouter

from src.users.auth import auth_backend
from src.users.dependencies import users_manager
from src.users.schemas import UserRead, UserCreate

router = APIRouter(prefix='/api')

auth_router = users_manager.get_auth_router(auth_backend)
auth_router.routes = [route for route in auth_router.routes if route.name != 'auth:jwt.logout']

router.include_router(
    auth_router,
    prefix='/auth/jwt',
    tags=['auth']
)

router.include_router(
    users_manager.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
