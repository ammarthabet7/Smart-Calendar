from backend.services.tts_service import tts_service

print("[TEST] Testing TTS Service...")
print("\n" + "="*50)

# Test 1: Simple speech
print("\n[TEST 1] Speaking simple message")
tts_service.speak("Hello, this is your appointment assistant.")

print("\n" + "="*50)

# Test 2: Appointment confirmation
print("\n[TEST 2] Speaking appointment confirmation")
tts_service.speak("Your appointment is confirmed for October 29th at 2 PM with John Doe.")

print("\n[TEST] TTS tests complete!")
