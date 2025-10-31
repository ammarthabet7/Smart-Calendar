from backend.services.llm_service import llm_service

print("[TEST] Testing LLM Service...")
print("\n" + "="*50)

# Test 1: List appointments
print("\n[TEST 1] List appointments request")
result = llm_service.parse_intent("What's my schedule for tomorrow?")
print(f"Result: {result}")

print("\n" + "="*50)

# Test 2: Book appointment with all details
print("\n[TEST 2] Complete booking request")
result = llm_service.parse_intent("Book John Doe at 2pm tomorrow")
print(f"Result: {result}")

print("\n" + "="*50)

# Test 3: Out of scope
print("\n[TEST 3] Out of scope request")
result = llm_service.parse_intent("What's the weather today?")
print(f"Result: {result}")

print("\n" + "="*50)

# Test 4: Unclear speech
print("\n[TEST 4] Unclear/empty input")
result = llm_service.parse_intent("uh")
print(f"Result: {result}")

print("\n" + "="*50)

# Test 5: Generate response
print("\n[TEST 5] Response generation")
context = {
    "action": "appointment_booked",
    "date": "2025-10-29",
    "time": "14:00",
    "patient_name": "John Doe"
}
response = llm_service.generate_response(context)
print(f"Response: {response}")

print("\n[TEST] All tests complete!")
