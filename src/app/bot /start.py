from aiogram import Router, types
from app.db.session import SessionLocal
from app.db.models import User
from app.bot.keyboards.menu import main_menu

router = Router()

@router.callback_query(lambda c: c.data=="recheck_channels")
async def recheck_channels(call: types.CallbackQuery):
    await call.message.answer("✅ Thanks! Now you have full access.", reply_markup=main_menu())
