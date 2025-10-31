from backend.services.calendar_service import calendar_service
from datetime import datetime, timedelta

print("[TEST] Testing Mock Calendar Service...")
print("\n" + "="*50)

# Test 1: List calendars
print("\n[TEST 1] List calendars")
calendars = calendar_service.list_calendars()
print(f"Found {len(calendars)} calendar(s)")

print("\n" + "="*50)

# Test 2: List appointments for tomorrow
print("\n[TEST 2] List appointments for tomorrow")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
result = calendar_service.list_appointments(tomorrow)
print(f"Success: {result['success']}")
if result['success']:
    print(f"Found {result['count']} appointments:")
    for apt in result['appointments']:
        print(f"  - {apt['time']}: {apt['patient_name']}")

print("\n" + "="*50)

# Test 3: Check availability (should be taken)
print("\n[TEST 3] Check availability for taken slot")
result = calendar_service.check_availability(tomorrow, "09:00")
print(f"Available: {result.get('available')} - Reason: {result.get('reason', 'N/A')}")

print("\n" + "="*50)

# Test 4: Check availability (should be free)
print("\n[TEST 4] Check availability for free slot")
result = calendar_service.check_availability(tomorrow, "15:00")
print(f"Available: {result.get('available')}")

print("\n" + "="*50)

# Test 5: Book appointment
print("\n[TEST 5] Book new appointment")
result = calendar_service.book_appointment(tomorrow, "15:00", "John Doe")
print(f"Success: {result['success']}")
if result['success']:
    print(f"Event ID: {result['event_id']}")

print("\n" + "="*50)

# Test 6: Try to book same slot (should fail - double booking)
print("\n[TEST 6] Try double booking")
result = calendar_service.book_appointment(tomorrow, "15:00", "Jane Doe")
print(f"Success: {result['success']} - Error: {result.get('error', 'N/A')}")

print("\n[TEST] All calendar tests complete!")
