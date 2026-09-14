from .health import router as health_router
from .bot import router as bot_router
from .guilds import router as guilds_router
from .moderation import router as moderation_router
from .leveling import router as leveling_router
from .tickets import router as tickets_router
from .verification import router as verification_router
from .automation import router as automation_router
from .ai import router as ai_router
from .youtube import router as youtube_router
from .minecraft import router as minecraft_router
from .admin import router as admin_router
from .backup import router as backup_router
from .analytics import router as analytics_router
from .autoresponder import router as autoresponder_router
from .antiphishing import router as antiphishing_router
from .templates import router as templates_router
from .antinuke import router as antinuke_router
from .onboarding import router as onboarding_router

all_routers = [
    health_router,
    bot_router,
    guilds_router,
    moderation_router,
    leveling_router,
    tickets_router,
    verification_router,
    automation_router,
    ai_router,
    youtube_router,
    minecraft_router,
    admin_router,
    backup_router,
    analytics_router,
    autoresponder_router,
    antiphishing_router,
    templates_router,
    antinuke_router,
    onboarding_router,
]


