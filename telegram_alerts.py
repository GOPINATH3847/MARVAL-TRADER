import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=bot_token)

def send_alert(message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print("Telegram error:", e)
