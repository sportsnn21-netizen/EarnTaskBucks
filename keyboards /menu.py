from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Get Tasks", callback_data="get_tasks"),
        InlineKeyboardButton("My Referrals", callback_data="my_referrals"),
        InlineKeyboardButton("Withdraw", callback_data="withdraw")
    )
    return kb
