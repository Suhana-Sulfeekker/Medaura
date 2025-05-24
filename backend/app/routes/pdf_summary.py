from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.models.chat_models import PDFSummaryResponse
from app.services.llm_service import get_llm_response
from app.db.mongodb import pdf_collection
from datetime import datetime, timezone
import pdfplumber
import io

router = APIRouter()

@router.post("/", response_model=PDFSummaryResponse)
async def pdf_summary(sessionId: str = Form(...), file: UploadFile = File(...)):
    if not sessionId or not file:
        raise HTTPException(status_code=400, detail="Missing sessionId or file.")

    try:
        contents = await file.read()
        
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            texts = [page.extract_text() for page in pdf.pages]
        full_text = "\n".join(filter(None, texts)).strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

    if not full_text:
        raise HTTPException(status_code=400, detail="No text extracted from PDF.")

    system_prompt = {
    "role": "system",
    "content": (
        "You are a compassionate doctor reviewing a medical report for a patient. Explain the findings clearly, concisely, and in simple language. "
        "Summarize the key points using bullet points. Provide brief, actionable suggestions when possible. "
        "Avoid medical jargon unless necessary, and keep the tone reassuring and helpful."
    )
    }

    user_prompt = {
        "role": "user",
        "content": f"Please summarize the following document:\n{full_text}"
    }
    messages = [system_prompt, user_prompt]

    try:
        summary = await get_llm_response(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM summary failed: {str(e)}")

    doc = {
        "sessionId": sessionId,
        "input_text": full_text,
        "summary": summary,
        "timestamp": datetime.now(timezone.utc),
    }
    try:
        await pdf_collection.insert_one(doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB insert failed: {str(e)}")

    return PDFSummaryResponse(summary=summary)
