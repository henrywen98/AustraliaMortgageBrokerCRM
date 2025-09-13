from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .clients import router as clients_router
from .deals import router as deals_router
from .tasks import router as tasks_router
from .stats import router as stats_router
from .exports import router as exports_router


api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(clients_router, prefix="/clients", tags=["clients"])
api_router.include_router(deals_router, prefix="/deals", tags=["deals"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(stats_router, prefix="/stats", tags=["stats"])
api_router.include_router(exports_router, prefix="/exports", tags=["exports"])

