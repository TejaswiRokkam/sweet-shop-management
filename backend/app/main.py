from fastapi import FastAPI
from app.database import Base, engine
from app.routes_auth import router as auth_router

app = FastAPI(title="Sweet Shop Management System")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
