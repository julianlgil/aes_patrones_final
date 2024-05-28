import asyncio
import threading

from fastapi import FastAPI

from .rabbit import subscribe_queue

app = FastAPI()


async def run_subscribe():
    await subscribe_queue()


def run_loop():
    asyncio.run(run_subscribe())


@app.on_event("startup")
def startup_event():
    subscribe_thread = threading.Thread(target=run_loop)
    subscribe_thread.daemon = True
    subscribe_thread.start()
