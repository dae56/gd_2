import redis.asyncio as redis

import sys

sys.path.append('src')

from app.env import REDIS_URL

cache_redis = redis.from_url(REDIS_URL)  # Подключение для Redis
