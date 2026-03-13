import os
import logging
import asyncio
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from telegram import Update, WebAppInfo, MenuButtonWebApp, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ─── Config ───
BOT_TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", 8080))

# Railway auto-provides RAILWAY_PUBLIC_DOMAIN
DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
APP_URL = os.environ.get("APP_URL", f"https://{DOMAIN}" if DOMAIN else "")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("oblik")

# ─── Simple HTTP Server (serves index.html) ───
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.dirname(os.path.abspath(__file__)), **kw)
    
    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        return super().do_GET()
    
    def log_message(self, fmt, *args):
        pass  # silence logs

def start_http():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    log.info(f"🌐 HTTP server on port {PORT}")
    server.serve_forever()

# ─── Bot Commands ───
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("📊 Відкрити ОБЛІК", web_app=WebAppInfo(url=APP_URL))
    ]])
    await update.message.reply_text("Натисни кнопку щоб відкрити трекер:", reply_markup=kb)

async def on_ready(app):
    try:
        await app.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(text="ОБЛІК", web_app=WebAppInfo(url=APP_URL))
        )
        log.info(f"✅ Menu button → {APP_URL}")
    except Exception as e:
        log.warning(f"Menu button: {e}")

# ─── Main ───
def main():
    log.info(f"APP_URL = {APP_URL}")
    
    if not APP_URL:
        log.error("❌ No APP_URL or RAILWAY_PUBLIC_DOMAIN. Set APP_URL in Variables.")
        return

    # Start HTTP in background
    Thread(target=start_http, daemon=True).start()

    # Start bot (polling)
    app = Application.builder().token(BOT_TOKEN).post_init(on_ready).build()
    app.add_handler(CommandHandler("start", cmd_start))
    log.info("🤖 Bot started")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
