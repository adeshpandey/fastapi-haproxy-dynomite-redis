from fastapi import FastAPI
import aioredis
import asyncio
import logging
from pydantic import BaseModel
from logging.config import dictConfig


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "mycoolapp"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "mycoolapp": {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")
app = FastAPI()

@app.on_event('startup')
async def on_startup() -> None:
    app.state.redis = await aioredis.create_redis_pool('redis://haproxy:6379')


async def call_redis(obj, fname, *args) -> any:

    try:
        if(args):
            res = await getattr(obj, fname)(*args)
        else:
            res = await getattr(obj, fname)()
    except Exception as e:
        logger.info(("Exception....", e))
        app.state.redis.close()
        await app.state.redis.wait_closed()
        app.state.redis = await aioredis.create_redis_pool('redis://haproxy:6379')
        if(args):
            res = await getattr(app.state.redis, fname)(*args)
        else:
            res = await getattr(app.state.redis, fname)()

    return res


@app.get("/")
async def root(
):
    await asyncio.sleep(5)
    p = await call_redis(app.state.redis, "get", "age")
    await app.state.redis.set("age", 31)
    return {"message": "Hello World", "info": p}
