from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes_auth import router as auth_router
from app.routes_sweets import router as sweets_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sweet Shop Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(sweets_router, prefix="/api/sweets", tags=["Sweets"])

@app.get("/")
def health_check():
    return {"status": "ok"}
