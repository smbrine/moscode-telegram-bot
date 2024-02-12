import asyncio
import base64
import time
import uuid
from datetime import datetime
from base64 import b64encode

import faust
from time import perf_counter_ns

from telegram.constants import ParseMode

from app import settings
from bot.main import bot


class NewClient(faust.Record, serializer="json"):
    phone: int = None
    name: str | None = None
    message: str | None = None
    email: str | None = None


app = faust.App("moscode-queue", broker=f"kafka://{settings.KAFKA_URL}")
newclient = app.topic("telegram-newclient-notify", value_type=NewClient)
arbitrary = app.topic("telegram-arbitrary-data")


async def send_guarded_message(message: str) -> None:
    try:
        await bot.send_message(
            settings.ADMIN_CHAT_ID, message, parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as e:
        try:
            bot.send_message(
                settings.ADMIN_CHAT_ID,
                f"Tried to send this:\n\n{str(message)}\n\nUnsuccessful. Error:\n{e}",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        except Exception as e:
            bot.send_message(
                settings.ADMIN_CHAT_ID,
                f"Error with sending message:\n{e}",
                parse_mode=ParseMode.MARKDOWN_V2,
            )


@app.agent(newclient)
async def process_newclient(messages):
    async for msg in messages:
        start_time = perf_counter_ns()
        print(msg)
        tg_msg = f"We have a new client\! \nName: {msg.name} \nPhone: {msg.phone} \nEmail: {msg.email}" + (
            f"\nThey said: ```copy\n{msg.message}\n```"
            if msg.message
            else "\nNo message :\("
        )
        await send_guarded_message(tg_msg)
        execution_time = perf_counter_ns() - start_time
        sleep_duration = max(0, 5_000_000_000 - execution_time) / 1_000_000_000
        print(sleep_duration)
        await asyncio.sleep(sleep_duration)


@app.agent(arbitrary)
async def process_arbitrary(messages):
    async for msg in messages:
        await send_guarded_message(msg)


# @app.timer(interval=60*30)
# async def send_password():
#     code = f'{settings.SECRET_KEY}:{time.time()}'
#
#     encoded_code = b64encode(code.encode()).decode()
#
#     await bot.send_message(
#         settings.ADMIN_CHAT_ID,
#         encoded_code,
#         parse_mode=ParseMode.MARKDOWN_V2,
#     )

if __name__ == "__main__":
    app.main()
