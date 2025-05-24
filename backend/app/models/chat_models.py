from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional
from typing import List

class ChatRequest(BaseModel):
    message: str
    sessionId: str

class ChatResponse(BaseModel):
    reply: str


class SymptomAnalysisRequest(BaseModel):
    symptoms: str
    sessionId: str

class SymptomAnalysisResponse(BaseModel):
    diseases: str




class PDFSummaryResponse(BaseModel):
    summary: str
