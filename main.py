import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Basic storage (Use a database like PostgreSQL for production)
user_files = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 **Dropbbox_BOT Ready**\n\n"
        "Send me a file and I will store it.\n"
        "Use /files to see your stored items."
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    file = update.message.effective_attachment
    
    # Store the file_id and file_name
    if user_id not in user_files:
        user_files[user_id] = []
    
    file_info = {"id": file.file_id, "name": getattr(file, 'file_name', 'Unknown File')}
    user_files[user_id].append(file_info)
    
    await update.message.reply_text(f"✅ Stored: {file_info['name']}")

async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    files = user_files.get(user_id, [])
    
    if not files:
        await update.message.reply_text("📂 You have no stored files.")
        return

    msg = "📂 **Your Stored Files:**\n"
    for i, f in enumerate(files, 1):
        msg += f"{i}. {f['name']}\n"
    
    await update.message.reply_text(msg)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("files", list_files))
    application.add_handler(MessageHandler(filters.ATTACHMENT | filters.PHOTO | filters.VIDEO, handle_file))
    
    print("Bot is running...")
    application.run_polling()
