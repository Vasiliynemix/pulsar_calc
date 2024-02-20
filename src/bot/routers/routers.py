from src.bot.routers.start import router as start_router
from src.bot.routers.admin import router as admin_router
from src.bot.routers.user import router as user_router

routers = (
    start_router,
    admin_router,
    user_router,
)
