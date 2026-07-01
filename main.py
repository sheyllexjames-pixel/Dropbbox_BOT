import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 **Dropbbox_BOT Ready**\n\n"
        "Send me any file (document, photo, video) and I will securely 'store' it for you!\n"
        "Use /files to see your storage."
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This captures documents, photos, and videos sent to the bot
    file = update.message.effective_attachment
    
    # In a real app, you'd save this to a database or cloud storage here
    # For now, we acknowledge receipt
    await update.message.reply_text(f"✅ File received and stored! (File ID: {file.file_id})")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    # This filter captures any type of document, video, or photo
    application.add_handler(MessageHandler(filters.ATTACHMENT | filters.PHOTO | filters.VIDEO, handle_file))
    
    print("Bot is running...")
    application.run_polling()
