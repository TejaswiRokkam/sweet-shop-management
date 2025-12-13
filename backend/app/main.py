from fastapi import FastAPI
from app.database import Base, engine

app = FastAPI(title="Sweet Shop Management System")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok"}
