from fastapi import FastAPI
from database import engine, Base
from routers.auth_routers import auth_router

app = FastAPI()

app.include_router(auth_router)

Base.metadata.create_all(bind=engine)