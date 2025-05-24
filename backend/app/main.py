from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, symptom, pdf_summary

app = FastAPI(title="Medaura Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(symptom.router, prefix="/symptom-analysis", tags=["symptom-analysis"])
app.include_router(pdf_summary.router, prefix="/pdf-summary", tags=["pdf-summary"])