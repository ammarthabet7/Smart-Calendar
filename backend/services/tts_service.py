import pyttsx3
import requests
from backend.config import settings
import tempfile
import os
import pygame
import re


class TTSService:
    """Text-to-speech service with multiple engine support"""
    
    def __init__(self):
        self.pyttsx3_engine = pyttsx3.init()
        self.pyttsx3_engine.setProperty('rate', 175)
        self.pyttsx3_engine.setProperty('volume', 1.0)
        
        pygame.mixer.init()
        
        self.elevenlabs_api_key = settings.ELEVENLABS_API_KEY
        self.elevenlabs_voice_id = "21m00Tcm4TlvDq8ikWAM"
        
        print("[TTS] Service initialized")
    
    def _clean_text_for_speech(self, text):
        """Remove markdown"""
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('_', ' ')
        text = text.replace('#', '')
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        return text.strip()
    
    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3"""
        try:
            print("[TTS] Using pyttsx3")
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
        except Exception as e:
            print(f"[TTS] pyttsx3 error: {e}")
    
    def _speak_elevenlabs(self, text):
        """Speak using ElevenLabs"""
        try:
            print("[TTS] Calling ElevenLabs...")
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name
            
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            os.remove(tmp_path)
            print("[TTS] ElevenLabs done")
            
        except Exception as e:
            print(f"[TTS] ElevenLabs error: {e}")
            raise
    
    def speak(self, text):
        """Speak text using pyttsx3"""
        cleaned_text = self._clean_text_for_speech(text)
        
        try:
            self._speak_pyttsx3(cleaned_text)
        except Exception as e:
            print(f"[TTS] Failed to speak: {e}")





tts_service = TTSService()
