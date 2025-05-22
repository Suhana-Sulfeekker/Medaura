from fastapi import APIRouter
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.llm_service import get_llm_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    system_prompt = {
        "role": "system",
        "content": (
            "You are a knowledgeable and trusted medical assistant developed for Medaura, specializing in healthcare and biomedical information. "
            "Your goal is to provide clear, accurate, and helpful explanations to users' health-related questions. Use precise medical terminology when appropriate, "
            "but ensure your answers remain easy to understand for a general audience."
        ),
    }
    
    messages = [
        system_prompt,
        {"role": "user", "content": request.message},
    ]
    
    reply = await get_llm_response(messages)
    return ChatResponse(reply=reply)
