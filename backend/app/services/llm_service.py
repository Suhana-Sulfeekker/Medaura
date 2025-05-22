from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

client = InferenceClient(
    model="aaditya/Llama3-OpenBioLLM-70B",
    token=os.getenv("HF_API_KEY"),  
)

async def get_llm_response(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model="aaditya/Llama3-OpenBioLLM-70B",
        messages=messages,
    )
    return response.choices[0].message.content.strip()
