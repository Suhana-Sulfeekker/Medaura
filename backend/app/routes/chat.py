from fastapi import APIRouter, HTTPException
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.llm_service import get_llm_response
from app.db.mongodb import chat_collection, symptom_collection, pdf_collection
from datetime import datetime, timezone

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    if not request.sessionId:
        raise HTTPException(status_code=400, detail="Missing sessionId in request.")

    
    system_prompt = {
        "role": "system",
        "content": (
            "You are a helpful and trusted medical assistant for Medaura. "
            "Provide concise, clear, and easy-to-read responses similar to ChatGPT style. "
            "Use bullet points and short paragraphs where appropriate. Avoid long, dense blocks of text."
        ),
    }

    messages = [system_prompt]

    try:
    
        chat_docs = await chat_collection.find_one({"sessionId": request.sessionId}) or {}
        symptom_docs = await symptom_collection.find({"sessionId": request.sessionId}).to_list(length=100)
        pdf_docs = await pdf_collection.find({"sessionId": request.sessionId}).to_list(length=100)


        combined_history = []


        if "chat_log" in chat_docs:
            for entry in chat_docs["chat_log"]:
                combined_history.append({
                    "timestamp": entry.get("timestamp"),
                    "role": "user",
                    "content": entry.get("user_message"),
                })
                combined_history.append({
                    "timestamp": entry.get("timestamp"),
                    "role": "assistant",
                    "content": entry.get("model_reply"),
                })

        
        for doc in symptom_docs:
            ts = doc.get("timestamp")
            combined_history.append({
                "timestamp": ts,
                "role": "user",
                "content": f"Symptoms: {doc.get('symptoms')}"
            })
            combined_history.append({
                "timestamp": ts,
                "role": "assistant",
                "content": doc.get("response")
            })

        
        for doc in pdf_docs:
            ts = doc.get("timestamp")
            combined_history.append({
                "timestamp": ts,
                "role": "user",
                "content": "Uploaded a document for summary."
            })
            combined_history.append({
                "timestamp": ts,
                "role": "assistant",
                "content": doc.get("summary")
            })

    
        combined_history.sort(key=lambda x: x["timestamp"])

    
        for msg in combined_history:
            if msg["content"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB read failed: {str(e)}")

    
    messages.append({"role": "user", "content": request.message})


    reply = await get_llm_response(messages)

    
    chat_entry = {
        "user_message": request.message,
        "model_reply": reply,
        "timestamp": datetime.now(timezone.utc)
    }

    try:
        await chat_collection.update_one(
            {"sessionId": request.sessionId},
            {
                "$setOnInsert": {
                    "sessionId": request.sessionId,
                    "created_at": datetime.now(timezone.utc)
                },
                "$push": {"chat_log": chat_entry}
            },
            upsert=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB update failed: {str(e)}")

    return ChatResponse(reply=reply)
