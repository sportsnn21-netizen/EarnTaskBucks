from aiogram import Router, types
from app.db.session import SessionLocal
from app.db.models import User

router = Router()

@router.message(commands=["start"])
async def start_command(message: types.Message):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id==str(message.from_user.id)).first()
    if not user:
        user = User(telegram_id=str(message.from_user.id), username=message.from_user.username)
        # check if user has referral code
        ref_id = None
        if message.get_args():
            ref_id = message.get_args()
            user.referred_by = int(ref_id)
        db.add(user)
        db.commit()
        # auto reward referral
        if ref_id:
            ref_user = db.query(User).filter(User.id==int(ref_id)).first()
            if ref_user:
                ref_user.balance += 5.0  # referral reward 5 BDT
                ref_user.referrals_count += 1
                db.commit()
    db.close()
    await message.answer("Welcome to EarnTaskBot! ✅ Use /menu to see available tasks and earn money.")
