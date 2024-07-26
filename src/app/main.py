from fastapi import FastAPI
import uvicorn

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

import sys

sys.path.append('src')

from app.multipart.routes.auth import router as auth_router
from app.multipart.routes.task import router as task_router


limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])  # Настройка количества запросов в минуту

app = FastAPI(
    title='GD2',
    version='0.0.1'
)

  # Подключение ограничений по количеству запросов
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

  # Добавление роутов
app.include_router(auth_router)
app.include_router(task_router)


if __name__ == '__main__':
    uvicorn.run(app=app)
