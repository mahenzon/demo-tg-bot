__all__ = ("router",)

from aiogram import Router

from .admin_handlers import router as admin_router
from .callback_handlers import router as callback_router
from .commands import router as commands_router
from .common import router as common_router
from .media_handlers import router as media_router

router = Router(name=__name__)

router.include_routers(
    callback_router,
    commands_router,
    media_router,
    admin_router,
)

# this one has to be the last!
router.include_router(common_router)
