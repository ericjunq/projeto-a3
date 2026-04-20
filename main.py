from fastapi import FastAPI
from database import engine, Base
from routers.auth_routers import auth_router
from routers.upload import router as upload_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(upload_router, prefix="/images", tags=["Images"])
app.include_router(upload_router, prefix="/user", tags=["Users"])

Base.metadata.create_all(bind=engine)