from aiogram import Router, types
from app.db.session import SessionLocal
from app.db.models import Task, User, UserTask
from app.bot.keyboards.menu import main_menu

router = Router()

@router.callback_query(lambda c: c.data=="get_tasks")
async def get_tasks(call: types.CallbackQuery):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id==str(call.from_user.id)).first()
    tasks = db.query(Task).all()
    for task in tasks:
        already_clicked = db.query(UserTask).filter(UserTask.user_id==user.id, UserTask.task_id==task.id).first()
        if not already_clicked:
            user.balance += task.reward
            db.add(UserTask(user_id=user.id, task_id=task.id, completed=True))
            db.commit()
        await call.message.answer(f"📝 {task.title}\nReward: {task.reward} BDT\n{task.description}\n{task.url}")
    db.close()
    await call.message.answer("✅ Tasks rewarded! Use /menu to return.", reply_markup=main_menu())
