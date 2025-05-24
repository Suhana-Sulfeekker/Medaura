from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

symptom_collection = db["symptom_diagnoses"]
chat_collection = db["chat_history"]
pdf_collection=db["pdf_summary"]