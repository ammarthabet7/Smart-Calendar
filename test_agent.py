from backend.agent.agent import appointment_agent

print("[TEST] Testing Appointment Agent with LangGraph")
print("="*60)

# Test 1: List appointments
print("\n[TEST 1] List appointments")
result = appointment_agent.process_message("What's my schedule for tomorrow?")
print(f"Response: {result['response']}\n")

input("Press Enter to continue to Test 2...")

# Test 2: Book appointment with all details
print("\n[TEST 2] Book appointment")
result = appointment_agent.process_message("Book John Smith at 3pm tomorrow")
print(f"Response: {result['response']}\n")

input("Press Enter to continue to Test 3...")

# Test 3: Out of scope
print("\n[TEST 3] Out of scope request")
result = appointment_agent.process_message("What's the weather?")
print(f"Response: {result['response']}\n")

input("Press Enter to continue to Test 4...")

# Test 4: Missing information
print("\n[TEST 4] Incomplete booking request")
result = appointment_agent.process_message("Book an appointment tomorrow")
print(f"Response: {result['response']}\n")

print("[TEST] Agent tests complete!")
