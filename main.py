import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. Load variables from Render's Environment (or .env if present)
load_dotenv()

# 2. Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 3. Welcome Message
WELCOME_MSG = (
    "Welcome to Dropbbox_BOT! 📦\n\n"
    "Store, sync, and organize your files across all devices.\n"
    "Features: Real-time sync, Auto-backups, File recovery, and Secure sharing."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📂 My Files", callback_data="my_files")],
        [InlineKeyboardButton("🔄 Sync/Backup", callback_data="sync"),
         InlineKeyboardButton("🔗 Share Files", callback_data="share")]
    ]
    await update.message.reply_text(WELCOME_MSG, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "my_files":
        await query.edit_message_text("📂 Access your organized documents, photos, and videos here.")
    elif query.data == "sync":
        await query.edit_message_text("🔄 Real-time synchronization active. Automatic backups running.")
    elif query.data == "share":
        await query.edit_message_text("🔗 Send a link to collaborate securely with others.")

if __name__ == '__main__':
    if not TOKEN:
        print("CRITICAL ERROR: TELEGRAM_BOT_TOKEN is missing!")
    else:
        # 4. Build and Run the Bot
        application = ApplicationBuilder().token(TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))
        
        print("Bot is running...")
        application.run_polling()
