from fastapi import APIRouter, HTTPException
from app.models.chat_models import SymptomAnalysisRequest, SymptomAnalysisResponse
from app.services.llm_service import get_llm_response
from app.db.mongodb import symptom_collection
from datetime import datetime, timezone

router = APIRouter()

@router.post("/", response_model=SymptomAnalysisResponse)
async def symptom_analysis(request: SymptomAnalysisRequest):
    if not request.sessionId or not request.symptoms:
        raise HTTPException(status_code=400, detail="Missing sessionId or symptoms.")

    system_prompt = {
        "role": "system",
        "content": (
            "You are a trusted medical assistant specialized in analyzing symptoms and suggesting possible diseases. "
            "Provide top 3 possible diseases in bullet points with small, easy-to-understand descriptions."
        )
    }

    user_prompt = {
        "role": "user",
        "content": f"Analyze these symptoms and list top 3 possible diseases with bullet points and concise explanations:\n{request.symptoms}"
    }

    messages = [system_prompt, user_prompt]

    try:
        reply = await get_llm_response(messages)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM request failed: {str(e)}")

    
    doc = {
        "sessionId": request.sessionId,
        "symptoms": request.symptoms,
        "response": reply,
        "timestamp": datetime.now(timezone.utc),
    }
    try:
        await symptom_collection.insert_one(doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB insert failed: {str(e)}")
    return SymptomAnalysisResponse(diseases=reply)
