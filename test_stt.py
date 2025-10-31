from backend.services.stt_service import stt_service

print("[TEST] Testing Speech-to-Text with Whisper")
print("="*60)
print("You have 5 seconds to speak after recording starts...")
print("Try saying: 'What's my schedule for tomorrow?'")
print()

input("Press Enter when ready...")

# Test listening
text = stt_service.listen_once()

if text:
    print(f"\n[SUCCESS] You said: '{text}'")
else:
    print("\n[FAILED] Could not capture speech")

print("\n[TEST] STT test complete!")
