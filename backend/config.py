import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    # OpenRouter API
    
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
    
    # Cronofy Calendar API
    #CRONOFY_ACCESS_TOKEN = os.getenv("CRONOFY_ACCESS_TOKEN")
    #CRONOFY_REFRESH_TOKEN = os.getenv("CRONOFY_REFRESH_TOKEN")
    #CRONOFY_API_URL = "https://api.cronofy.com/v1"
    
    # Clinic Configuration
    CLINIC_NAME = os.getenv("CLINIC_NAME", "HealthCare Clinic")
    CLINIC_HOURS_START = os.getenv("CLINIC_HOURS_START", "09:00")
    CLINIC_HOURS_END = os.getenv("CLINIC_HOURS_END", "18:00")
    APPOINTMENT_DURATION = int(os.getenv("APPOINTMENT_DURATION", "30"))
    
    # TTS Settings
    TTS_RATE = 150
    TTS_VOLUME = 1.0
    
    # Timeouts
    API_TIMEOUT = 10
    STT_TIMEOUT = 5
    
    @classmethod
    def validate(cls):
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not set in .env")
        if not cls.CRONOFY_ACCESS_TOKEN:
            raise ValueError("CRONOFY_ACCESS_TOKEN not set in .env")
        if not cls.ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY not set in .env")
        print("[CONFIG] Configuration loaded successfully")
import sys
import os

class SilentPrint:
    """Suppress print statements without affecting other functionality"""
    def write(self, text):
        pass  # Do nothing
    
    def flush(self):
        pass  # Do nothing
    
    def isatty(self):
        return False  # Required by uvicorn
    
    def fileno(self):
        return -1  # Required by some libraries



settings = Settings()
