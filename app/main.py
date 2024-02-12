import sys
import pathlib

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi import status

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from telegram import Update
from app import settings
from prometheus_fastapi_instrumentator import Instrumentator

project_dir = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))
from bot.main import bot


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    if bot:
        response = await bot.get_webhook_info()
        webhook_url = f"{settings.PUBLIC_ADDR}/webhook?token={settings.TG_BOT_TOKEN}"
        while response.url != webhook_url:
            await bot.set_webhook(url=webhook_url, allowed_updates=Update.ALL_TYPES)
            response = await bot.get_webhook_info()
            print(response)
        print(response)

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)
Instrumentator().instrument(app).expose(app)


@app.post("/webhook")
async def webhook(request: Request, token: str):
    if token != settings.TG_BOT_TOKEN:
        raise HTTPException(status_code=429)
    data = await request.json()
    await bot.send_message(855235544, str(data))
    return status.HTTP_200_OK


@app.get("/healthz")
async def healthz():
    return JSONResponse(status_code=200, content={"health": "ok"})


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.LISTEN_ADDR,
        port=settings.LISTEN_PORT,
        reload=settings.DEBUG,
        log_level=0,
        use_colors=True,
    )
