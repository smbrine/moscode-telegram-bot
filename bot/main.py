import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

bot = Bot(token=TG_BOT_TOKEN)
