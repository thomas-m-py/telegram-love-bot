from aiogram import Router
from src.bot.handlers.create_update_profile.start import router as start_router
from src.bot.handlers.create_update_profile.age import router as age_router
from src.bot.handlers.create_update_profile.sex import router as sex_router
from src.bot.handlers.create_update_profile.interest import router as interest_router
from src.bot.handlers.create_update_profile.city import router as city_router
from src.bot.handlers.create_update_profile.name import router as name_router
from src.bot.handlers.create_update_profile.bio import router as bio_router
from src.bot.handlers.create_update_profile.media import router as media_router
from src.bot.handlers.create_update_profile.confirmation import (
    router as confirmation_router,
)


router = Router()

router.include_router(start_router)
router.include_router(age_router)
router.include_router(sex_router)
router.include_router(interest_router)
router.include_router(city_router)
router.include_router(name_router)
router.include_router(bio_router)
router.include_router(media_router)
router.include_router(confirmation_router)
