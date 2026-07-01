import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DB_NAME = "storage.db"

# Database Setup
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS files (user_id INTEGER, file_name TEXT)')
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📂 My Files", callback_data="my_files")],
        [InlineKeyboardButton("🔄 Sync/Backup", callback_data="sync"),
         InlineKeyboardButton("🔗 Share Files", callback_data="share")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📦 **Dropbbox_BOT Ready**\n\nStore, sync, and organize your files.", reply_markup=reply_markup)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    file = update.message.effective_attachment
    file_name = getattr(file, 'file_name', f"File_{file.file_id[:8]}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO files (user_id, file_name) VALUES (?, ?)', (user_id, file_name))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(f"✅ Stored: {file_name}")

async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT file_name FROM files WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        await update.message.reply_text("📂 You have no stored files.")
    else:
        msg = "📂 **Your Stored Files:**\n" + "\n".join([f"• {row[0]}" for row in rows])
        await update.message.reply_text(msg)

if __name__ == '__main__':
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("files", list_files))
    application.add_handler(CallbackQueryHandler(lambda u, c: list_files(u, c) if u.callback_query.data == "my_files" else None))
    application.add_handler(MessageHandler(filters.ATTACHMENT | filters.PHOTO | filters.VIDEO, handle_file))
    print("Bot is running...")
    application.run_polling()
