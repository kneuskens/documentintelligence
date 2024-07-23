import os
import pydantic
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

def get_settings():
    return Settings()

class DocumentIntelligenceSettings(BaseSettings):
    api_key: str =os.getenv("DOCUMENT_INTELLIGENCE_API_KEY")
    endpoint: str =os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")

class Settings(BaseSettings):
    document_intelligence:DocumentIntelligenceSettings=DocumentIntelligenceSettings()