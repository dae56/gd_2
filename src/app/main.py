from fastapi import FastAPI
import uvicorn

import sys

sys.path.append('src')

from app.multipart.routes.auth import router as auth_router
from app.multipart.routes.task import router as task_router


app = FastAPI(
    title='GD2',
    version='0.0.1'
)

app.include_router(auth_router)
app.include_router(task_router)


if __name__ == '__main__':
    uvicorn.run(app=app,
                port=8080)