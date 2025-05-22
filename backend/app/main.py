from fastapi import FastAPI
from app.routes import chat

app = FastAPI(title="Medaura Backend")

# Include chat router
app.include_router(chat.router, prefix="/chat", tags=["chat"])
