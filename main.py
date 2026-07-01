import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") # Provided automatically by Render

# Initialize Telegram Bot Application
ptb = Application.builder().token(TOKEN).build()

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Dropbbox_BOT!\n"
        "Send me any file, photo, or document, and I will safely index and back it up for you."
    )

async def handle_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Telegram assigns a unique, persistent file_id to every file sent to it.
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file_size = update.message.document.file_size
    
    # TODO: In production, save these variables to a database (e.g., Supabase, MongoDB) 
    # to enable search, folder structures, and recovery logs.
    
    await update.message.reply_text(
        f"💾 **File Backed Up Successfully!**\n\n"
        f"📁 Name: {file_name}\n"
        f"⚖️ Size: {file_size} bytes\n"
        f"🔑 Index Key (ID): `{file_id}`\n\n"
        f"You can retrieve this file anytime via search or category menus."
    )

# --- Lifespan Management for Webhooks ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup webhook configuration when server starts
    await ptb.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()

# Initialize FastAPI App
app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def process_update(request: Request):
    req_json = await request.json()
    update = Update.de_json(req_json, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=200)

@app.get("/")
async def health_check():
    return {"status": "Dropbbox_BOT is up and running!"}

# Register Bot Event Handlers
ptb.add_handler(CommandHandler("start", start))
ptb.add_handler(MessageHandler(filters.Document.ALL, handle_docs))
