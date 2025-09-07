import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# ---------------------------
# CONFIG
# ---------------------------
BOT_TOKEN = os.getenv("8338228858:AAH_K8Hm5U5QRDiCiVCD83U_3Oidhw60RsA")
DB_URL = os.getenv("DB_URL")
WEBHOOK_URL = os.getenv("https://earntaskbucks. onrender. com /webhook")  # e.g., https://earntaskbucks.onrender.com/webhook

# ---------------------------
# LOGGING
# ---------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
def get_db_connection():
    conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
    return conn

# ---------------------------
# START COMMAND
# ---------------------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            username TEXT,
            balance NUMERIC DEFAULT 0,
            referral_id BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cur.execute(
        "INSERT INTO users (telegram_id, username) VALUES (%s, %s) ON CONFLICT (telegram_id) DO NOTHING",
        (user.id, user.username)
    )
    conn.commit()
    cur.close()
    conn.close()

    keyboard = [
        [InlineKeyboardButton("💰 Get Tasks / Earn", callback_data='get_tasks')],
        [InlineKeyboardButton("📊 My Earnings", callback_data='my_earnings')],
        [InlineKeyboardButton("📝 How It Works", callback_data='how_it_works')],
        [InlineKeyboardButton("🎯 Referral / Invite Friends", callback_data='referral')],
        [InlineKeyboardButton("💳 Withdraw / Payment", callback_data='withdraw')],
        [InlineKeyboardButton("❓ FAQ / Help", callback_data='faq')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to EarnQuick Bot! Select an option:", reply_markup=reply_markup)

# ---------------------------
# CALLBACK HANDLER
# ---------------------------
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'get_tasks':
        query.edit_message_text("Select a task type:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Home", callback_data='back_home')]]))
    elif data == 'my_earnings':
        query.edit_message_text("Your current earnings are: 0 USD (Demo)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Home", callback_data='back_home')]]))
    elif data == 'how_it_works':
        query.edit_message_text("Step-by-step guide: Click tasks -> Complete -> Earn", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Home", callback_data='back_home')]]))
    elif data == 'referral':
        query.edit_message_text("Your referral link: t.me/EarnQuick_OfficialBot?start=REF123", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Home", callback_data='back_home')]]))
    elif data == 'withdraw':
        query.edit_message_text("Withdraw options:\n💵 Bkash / Rocket / Nagad / Bank", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Home", callback_data='back_home')]]))
    elif data == 'faq':
        query.edit_message_text("FAQ:\n1. How to earn?\n2. How to withdraw?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Home", callback_data='back_home')]]))
    elif data == 'back_home':
        keyboard = [
            [InlineKeyboardButton("💰 Get Tasks / Earn", callback_data='get_tasks')],
            [InlineKeyboardButton("📊 My Earnings", callback_data='my_earnings')],
            [InlineKeyboardButton("📝 How It Works", callback_data='how_it_works')],
            [InlineKeyboardButton("🎯 Referral / Invite Friends", callback_data='referral')],
            [InlineKeyboardButton("💳 Withdraw / Payment", callback_data='withdraw')],
            [InlineKeyboardButton("❓ FAQ / Help", callback_data='faq')]
        ]
        query.edit_message_text("Welcome to EarnQuick Bot! Select an option:", reply_markup=InlineKeyboardMarkup(keyboard))

# ---------------------------
# MAIN
# ---------------------------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    
    # Webhook setup
    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get("PORT", 5000)),
                          url_path="webhook")
    updater.bot.set_webhook(WEBHOOK_URL)
    
    updater.idle()

if __name__ == '__main__':
    main()
