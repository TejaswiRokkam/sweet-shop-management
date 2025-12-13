from fastapi import FastAPI

app = FastAPI(title="Sweet Shop Management System")

@app.get("/")
def health_check():
    return {"status": "ok"}
