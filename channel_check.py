from aiogram import BaseMiddleware
from aiogram.types import Message
from app.core.config import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

class ChannelCheckMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id

        required_channels = settings.REQUIRED_CHANNELS
        not_joined = []

        for ch in required_channels:
            if "t.me" in ch or ch.startswith("@"):
                channel = ch.replace("https://t.me/", "").replace("@", "")
                try:
                    member = await self.bot.get_chat_member(channel, user_id)
                    if member.status in ["left", "kicked"]:
                        not_joined.append(ch)
                except Exception as e:
                    # যদি বট এডমিন না হয় তাহলে এই এক্সসেপশন আসতে পারে
                    not_joined.append(ch)
            else:
                # WhatsApp লিংক ডিরেক্টলি দেখানো হবে
                not_joined.append(ch)

        if not_joined:
            kb = InlineKeyboardMarkup()
            for link in not_joined:
                kb.add(InlineKeyboardButton("Join Now", url=link))
            kb.add(InlineKeyboardButton("✅ I've Joined", callback_data="recheck_channels"))
            await event.answer("🚨 You must join our channels first to use the bot.", reply_markup=kb)
            return
        return await handler(event, data)
