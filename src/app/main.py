from fastapi import FastAPI
import uvicorn


app = FastAPI(
    title='gd_task',
    version='0.1.0'
)


if __name__ == '__main__':
    uvicorn.run(app=app)
