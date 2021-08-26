from fastapi import FastAPI, Depends
import fastapi_plugins
import aioredis
import asyncio
app = FastAPI()


@app.on_event('startup')
async def on_startup() -> None:
    try:
        config = fastapi_plugins.RedisSettings(
            redis_url='redis://haproxy:6379', redis_db=None, redis_connection_timeout=2, redis_prestart_tries=5,)
        await fastapi_plugins.redis_plugin.init_app(app, config=config)
        await fastapi_plugins.redis_plugin.init()
    except Exception as e:
        raise


@app.get("/")
async def root(
        cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
):
    p = await cache.ping()
    return {"message": "Hello World %s" % p}
