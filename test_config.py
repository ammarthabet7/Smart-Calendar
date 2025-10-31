from backend.config import settings

print("[TEST] Testing configuration...")

try:
    settings.validate()
    print(f"[TEST] OpenRouter API Key: {settings.OPENROUTER_API_KEY[:20]}...")
    print(f"[TEST] Cronofy Token: {settings.CRONOFY_ACCESS_TOKEN[:20]}...")
    print(f"[TEST] Clinic Name: {settings.CLINIC_NAME}")
    print("[TEST] Configuration test PASSED")
except Exception as e:
    print(f"[TEST] Configuration test FAILED: {e}")
