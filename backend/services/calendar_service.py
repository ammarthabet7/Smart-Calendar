from datetime import datetime, timedelta
from backend.config import settings


class MockCalendarService:
    
    def __init__(self):
        self.appointments = self._initialize_mock_data()
        print("[CALENDAR] Mock calendar service initialized")
        print(f"[CALENDAR] Loaded {len(self.appointments)} mock appointments")
        
    def _parse_time_to_24h(self, time_str):
        """Convert time formats like '09:30 AM', '2 PM', '14:00' to 24-hour format HH:MM"""
        try:
            if not time_str:
                return None
            
            time_str = time_str.strip()
            
            # Remove extra spaces
            time_str = ' '.join(time_str.split())
            
            # Try 12-hour format with AM/PM first (e.g., "09:30 AM", "2 PM")
            if "AM" in time_str.upper() or "PM" in time_str.upper():
                # Handle both "09:30 AM" and "9 AM" formats
                try:
                    if ":" in time_str:
                        time_24 = datetime.strptime(time_str, "%I:%M %p").time()
                    else:
                        time_24 = datetime.strptime(time_str, "%I %p").time()
                    return time_24.strftime("%H:%M")
                except ValueError:
                    pass
            
            # Try 24-hour format (e.g., "14:00", "09:30")
            if ":" in time_str:
                parts = time_str.split(":")
                if len(parts) == 2:
                    hour = int(parts[0].strip())
                    minute = int(parts[1].strip())
                    if 0 <= hour <= 23 and 0 <= minute <= 59:
                        return f"{hour:02d}:{minute:02d}"
            
            print(f"[CALENDAR] Could not parse time: '{time_str}'")
            return None
        
        except Exception as e:
            print(f"[CALENDAR] Time parsing error for '{time_str}': {e}")
            return None

    
    def _initialize_mock_data(self):
        today = datetime.now()
        appointments = []
        
        tomorrow = today + timedelta(days=1)
        appointments.extend([
            {
                "id": "mock_1",
                "date": tomorrow.strftime("%Y-%m-%d"),
                "time": "09:00",
                "patient_name": "Alice Johnson",
                "duration": 30,
                "status": "confirmed"
            },
            {
                "id": "mock_2",
                "date": tomorrow.strftime("%Y-%m-%d"),
                "time": "10:30",
                "patient_name": "Bob Smith",
                "duration": 30,
                "status": "confirmed"
            },
            {
                "id": "mock_3",
                "date": tomorrow.strftime("%Y-%m-%d"),
                "time": "14:00",
                "patient_name": "Carol White",
                "duration": 30,
                "status": "confirmed"
            }
        ])
        
        day_after = today + timedelta(days=2)
        appointments.append({
            "id": "mock_4",
            "date": day_after.strftime("%Y-%m-%d"),
            "time": "11:00",
            "patient_name": "David Brown",
            "duration": 30,
            "status": "confirmed"
        })
        
        return appointments
    
    def list_calendars(self):
        print("[CALENDAR] Fetching calendar list...")
        return [{"calendar_id": "mock_cal_1", "name": "Primary Calendar"}]
    
    def list_appointments(self, date_str):
        print(f"[CALENDAR] Fetching appointments for {date_str}")
        
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print(f"[CALENDAR] Invalid date format: {date_str}")
            return {
                "success": False,
                "error": "invalid_date",
                "message": "Invalid date format"
            }
        
        day_appointments = [
            apt for apt in self.appointments 
            if apt["date"] == date_str and apt["status"] == "confirmed"
        ]
        
        print(f"[CALENDAR] Found {len(day_appointments)} appointments")
        
        return {
            "success": True,
            "appointments": day_appointments,
            "count": len(day_appointments)
        }

    def get_appointments(self, date_str=None):
        """Wrapper for list_appointments - returns appointments list directly"""
        if date_str:
            result = self.list_appointments(date_str)
            if result.get('success'):
                return result.get('appointments', [])
            else:
                return []
        else:
            # Return all future appointments
            from datetime import datetime
            today = datetime.now().date()
            return [
                apt for apt in self.appointments 
                if datetime.strptime(apt['date'], '%Y-%m-%d').date() >= today 
                and apt['status'] == 'confirmed'
            ]

    def check_availability(self, date_str, time_str):
        """Check if a time slot is available"""
        print(f"[CALENDAR] Checking availability for {date_str} at {time_str}")
        
        # Convert time to 24-hour format
        time_24h = self._parse_time_to_24h(time_str)
        if not time_24h:
            print(f"[CALENDAR] Invalid time format: {time_str}")
            return {
                "available": False,
                "reason": "invalid_time",
                "message": "Invalid time format"
            }
        
        try:
            clinic_start = datetime.strptime(settings.CLINIC_HOURS_START, "%H:%M").time()
            clinic_end = datetime.strptime(settings.CLINIC_HOURS_END, "%H:%M").time()
            target_time = datetime.strptime(time_24h, "%H:%M").time()
            
            if not (clinic_start <= target_time < clinic_end):
                print("[CALENDAR] Time outside business hours")
                return {
                    "available": False,
                    "reason": "outside_hours",
                    "message": f"Clinic hours are {settings.CLINIC_HOURS_START} to {settings.CLINIC_HOURS_END}"
                }
        except ValueError as e:
            print(f"[CALENDAR] Error checking hours: {e}")
            return {"available": False, "reason": "invalid_time"}
        
        # Check if slot is already booked
        for apt in self.appointments:
            if apt["date"] == date_str and apt["time"] == time_24h and apt["status"] == "confirmed":
                print("[CALENDAR] Time slot is already booked")
                return {
                    "available": False,
                    "reason": "booked",
                    "message": f"That time slot is already booked with {apt['patient_name']}"
                }
        
        print("[CALENDAR] Time slot is available")
        return {"available": True}

    def book_appointment(self, date_str, time_str, patient_name, duration=30):
        print(f"[CALENDAR] Booking appointment: {patient_name} on {date_str} at {time_str}")
        
        # Convert time to 24-hour format
        time_24h = self._parse_time_to_24h(time_str)
        if not time_24h:
            return {
                "success": False,
                "error": "invalid_time",
                "message": "Invalid time format"
            }
        
        availability = self.check_availability(date_str, time_24h)
        if not availability.get("available"):
            print("[CALENDAR] Slot not available")
            return {
                "success": False,
                "error": "slot_unavailable",
                "message": availability.get("message", "Time slot is not available")
            }
        
        event_id = f"mock_{len(self.appointments) + 1}"
        new_appointment = {
            "id": event_id,
            "date": date_str,
            "time": time_24h,
            "patient_name": patient_name,
            "duration": duration,
            "status": "confirmed"
        }
        
        self.appointments.append(new_appointment)
        print(f"[CALENDAR] Appointment booked successfully: {event_id}")
        
        return {
            "success": True,
            "event_id": event_id,
            "date": date_str,
            "time": time_24h,
            "patient_name": patient_name
        }

    def cancel_appointment(self, date_str, time_str=None, patient_name=None):
        """Cancel appointment by date and time or patient name"""
        print(f"[CALENDAR] Cancelling appointment: date={date_str}, time={time_str}, patient={patient_name}")
        
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return {
                "success": False,
                "error": "invalid_date",
                "message": "Invalid date format"
            }
        
        # Find appointment to cancel
        appointment_to_cancel = None
        
        # Search by date + time
        if time_str:
            time_24h = self._parse_time_to_24h(time_str)
            if time_24h:
                for apt in self.appointments:
                    if apt["date"] == date_str and apt["time"] == time_24h and apt["status"] == "confirmed":
                        appointment_to_cancel = apt
                        break
        
        # Search by date + patient name
        if not appointment_to_cancel and patient_name:
            for apt in self.appointments:
                if apt["date"] == date_str and apt["patient_name"].lower() == patient_name.lower() and apt["status"] == "confirmed":
                    appointment_to_cancel = apt
                    break
        
        # Search by patient name only (find earliest future appointment)
        if not appointment_to_cancel and patient_name:
            future_appointments = [
                apt for apt in self.appointments
                if apt["patient_name"].lower() == patient_name.lower() 
                and apt["status"] == "confirmed"
                and datetime.strptime(apt["date"], "%Y-%m-%d").date() >= datetime.now().date()
            ]
            if future_appointments:
                appointment_to_cancel = min(future_appointments, key=lambda x: (x["date"], x["time"]))
        
        if not appointment_to_cancel:
            print("[CALENDAR] No matching appointment found")
            return {
                "success": False,
                "error": "not_found",
                "message": "No matching appointment found to cancel"
            }
        
        # Mark as cancelled
        appointment_to_cancel["status"] = "cancelled"
        
        print(f"[CALENDAR] Appointment cancelled: {appointment_to_cancel['id']}")
        
        return {
            "success": True,
            "appointment": appointment_to_cancel,
            "message": f"Appointment cancelled for {appointment_to_cancel['patient_name']} on {appointment_to_cancel['date']} at {appointment_to_cancel['time']}"
        }


calendar_service = MockCalendarService()
