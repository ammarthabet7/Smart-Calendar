import sounddevice as sd
import soundfile as sf
import whisper
import tempfile
import os
import numpy as np
from backend.config import settings

class STTService:
    
    def __init__(self):
        # Initialize Whisper model
        print("[STT] Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        print("[STT] Whisper model loaded (base)")
        print("[STT] Speech recognition initialized with smart voice detection")
    
    def listen(self, max_duration=60, sample_rate=16000):
        """
        Record audio with smart voice activity detection
        - Waits for user to start speaking
        - Records everything user says
        - Stops after 3 seconds of silence
        - Max duration: 60 seconds (safety limit)
        """
        print(f"[STT] 🎤 Listening... Speak naturally. Will stop after 3s of silence.")
        
        try:
            # VAD parameters
            silence_threshold = 0.015      # Amplitude threshold for silence (tuned for normal speech)
            silence_duration = 1.5         # Seconds of silence before stopping
            chunk_duration = 0.1           # Process in 100ms chunks
            min_speech_duration = 0.5      # Need at least 0.5s of speech before considering stopping
            
            chunk_size = int(chunk_duration * sample_rate)
            silent_chunks = 0
            max_silent_chunks = int(silence_duration / chunk_duration)
            min_speech_chunks = int(min_speech_duration / chunk_duration)
            
            audio_chunks = []
            has_speech = False
            speech_chunks = 0
            
            # Start recording in chunks
            with sd.InputStream(samplerate=sample_rate, channels=1, dtype='float32') as stream:
                print("[STT] 🔴 Recording started...")
                
                for i in range(int(max_duration / chunk_duration)):
                    chunk, _ = stream.read(chunk_size)
                    audio_chunks.append(chunk)
                    
                    # Calculate volume level
                    volume = np.abs(chunk).mean()
                    
                    # Check if there's sound (above threshold)
                    if volume > silence_threshold:
                        silent_chunks = 0
                        speech_chunks += 1
                        if not has_speech and speech_chunks >= 3:  # At least 0.3s of sound
                            has_speech = True
                            print("[STT] 🗣️  Speech detected, recording...")
                    else:
                        # Silence detected
                        if has_speech and speech_chunks >= min_speech_chunks:
                            silent_chunks += 1
                    
                    # Stop if we've detected speech and then 3 seconds of silence
                    if has_speech and silent_chunks >= max_silent_chunks:
                        duration = len(audio_chunks) * chunk_duration
                        print(f"[STT] ✓ Recording stopped after {duration:.1f}s (3s silence detected)")
                        break
                
                # If loop completed without stopping
                if silent_chunks < max_silent_chunks:
                    print(f"[STT] ✓ Recording stopped at max duration ({max_duration}s)")
            
            # Check if we got any speech
            if not has_speech or len(audio_chunks) < min_speech_chunks:
                print("[STT] ⚠️  No speech detected")
                return None
            
            # Combine all chunks
            audio = np.concatenate(audio_chunks)
            
            print("[STT] 🔄 Transcribing with Whisper...")
            
            # Save to temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_path = tmp_file.name
            
            sf.write(tmp_path, audio, sample_rate)
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(tmp_path, language='en', fp16=False)
            text = result['text'].strip()
            
            # Clean up
            os.remove(tmp_path)
            
            if text and len(text) > 1:
                print(f"[STT] ✅ Recognized: '{text}'")
                return text
            else:
                print("[STT] ⚠️  No text transcribed")
                return None
                
        except Exception as e:
            print(f"[STT] ❌ Error: {e}")
            return None
    
    def listen_once(self):
        """Single listening session with smart voice detection"""
        return self.listen(max_duration=60)

stt_service = STTService()
