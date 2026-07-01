import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Temporary memory (Note: This will reset if the bot restarts)
user_files = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This matches the menu buttons from your reference image
    keyboard = [
        [InlineKeyboardButton("📂 My Files", callback_data="my_files")],
        [InlineKeyboardButton("🔄 Sync/Backup", callback_data="sync"),
         InlineKeyboardButton("🔗 Share Files", callback_data="share")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to Dropbbox_BOT! 📦\n\n"
        "Store, sync, and organize your files across all devices.", 
        reply_markup=reply_markup
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    # Get the file name if it's a document, otherwise use a default
    file = update.message.effective_attachment
    file_name = getattr(file, 'file_name', f"File_{file.file_id[:8]}")

    if user_id not in user_files:
        user_files[user_id] = []
    
    user_files[user_id].append(file_name)
    await update.message.reply_text(f"✅ Stored: {file_name}")

async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    files = user_files.get(user_id, [])
    
    if not files:
        await update.message.reply_text("📂 You have no stored files.")
    else:
        msg = "📂 **Your Stored Files:**\n" + "\n".join([f"• {f}" for f in files])
        await update.message.reply_text(msg)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "my_files":
        await list_files(update, context)
    else:
        await query.edit_message_text(f"Feature '{query.data}' is under development.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("files", list_files))
    application.add_handler(CallbackQueryHandler(button_handler))
    # This captures documents, photos, and videos
    application.add_handler(MessageHandler(filters.ATTACHMENT | filters.PHOTO | filters.VIDEO, handle_file))
    
    application.run_polling()
