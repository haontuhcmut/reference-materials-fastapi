import redis.asyncio as aioredis

from app.config import Config

JTI_EXPIRY = 3600

token_blocklist = aioredis.from_url(Config)