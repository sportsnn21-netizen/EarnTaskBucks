from aiogram import Router, types
from app.bot.keyboards.menu import main_menu

router = Router()

@router.message(commands=["menu"])
async def menu_command(message: types.Message):
    await message.answer("Main Menu:", reply_markup=main_menu())
