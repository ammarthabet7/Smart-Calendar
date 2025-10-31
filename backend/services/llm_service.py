import requests
import json
from backend.config import settings


class LLMService:
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "qwen/qwen-2.5-72b-instruct"
        print("[LLM] Service initialized with Qwen 2.5 72B")
    
    def parse_intent(self, user_message, conversation_history=None):
        """Parse user intent with retry logic and conversation context"""
        
        today_str = "2025-10-31 (Friday)"
        tomorrow_str = "2025-11-01 (Saturday)"
        
        context = ""
        if conversation_history and isinstance(conversation_history, list):
            try:
                context = "\n".join([
                    f"User: {turn.get('user', '') if isinstance(turn, dict) else ''}\nAgent: {turn.get('agent', '') if isinstance(turn, dict) else ''}" 
                    for turn in conversation_history[-3:] if isinstance(turn, dict)
                ])
            except Exception as e:
                print(f"[LLM] Error building context: {e}")
                context = ""
        
        system_prompt = """You are an AI scheduling assistant for a medical clinic. You help RECEPTIONISTS manage appointments for multiple patients.

DATE PARSING EXAMPLES:
- Today is 2025-10-31 (Friday)
- "tomorrow" = 2025-11-01 (Saturday)
- "next Friday" = the upcoming Friday from today
- "this Friday" = the upcoming Friday (same as next Friday if today is before Friday)
- "Friday" without context = the upcoming Friday
- Be consistent with relative date interpretation

CRITICAL: Identify the CORRECT INTENT:

1. "list_appointments" - User wants to SEE/VIEW/SHOW/LIST appointments
   - Keywords: "show me", "what's on", "list", "view", "display", "appointments"
   - Examples: "Show me appointments", "What's on the schedule for Friday?", "List all appointments"
   - Response: Return list_appointments intent with date or date range
   
2. "book_appointment" - User wants to CREATE/BOOK/SCHEDULE a NEW appointment
   - Keywords: "book", "schedule", "make an appointment", "reserve", "create"
   - Examples: "Book John at 2pm", "Schedule an appointment", "I need to schedule someone"
   - Response: Return book_appointment with date, time, patient_name
   
3. "cancel_appointment" - User wants to CANCEL/DELETE/REMOVE an appointment
   - Keywords: "cancel", "remove", "delete", "reschedule", "unbook"
   - Examples: "Cancel John's appointment", "Remove the 2pm slot"
   - Response: Return cancel_appointment intent
   
4. "check_availability" - User asks IF a slot is FREE
   - Keywords: "available", "free", "is", "do you have", "can we"
   - Examples: "Is 2pm free?", "Do you have availability on Friday?"
   - Response: Return check_availability with date and time
   
5. "system_info" - Questions about YOU (the assistant)
   - Keywords: "what's your name", "who are you", "what can you do"
   - Response: Return system_info with helpful message
   
6. "out_of_scope" - ONLY completely irrelevant topics (weather, sports, jokes)
   - Response: Politely redirect to appointment scheduling

IMPORTANT CONTEXT:
- The user is a RECEPTIONIST, not a patient
- Receptionist specifies patient names when booking
- Extract information from current AND previous conversation turns
- Be smart about date parsing: "tomorrow", "next Monday", "October 30", "the 30th" all valid
- Time formats: "2pm", "14:00", "2 o'clock", "6pm" all valid
- If information was provided earlier in conversation, extract it from history

Intent types:
- "book_appointment": Book/schedule new appointment
- "list_appointments": View/show appointments
  * For SINGLE date: return "date" field with specific date
  * For DATE RANGE: return "start_date" and "end_date" fields
  * For ALL appointments: set all date fields to null
- "check_availability": Check if time slot is free
- "cancel_appointment": Cancel existing appointment
- "system_info": Questions about the system itself
- "out_of_scope": Completely unrelated topics

EXAMPLES:

Receptionist: "Show all appointments for the next 5 days"
{"intent": "list_appointments", "date": null, "start_date": "2025-10-31", "end_date": "2025-11-04", "time": null, "patient_name": null, "clarification_needed": false, "missing_fields": []}

Receptionist: "List appointments from October 29 to November 2"
{"intent": "list_appointments", "date": null, "start_date": "2025-10-29", "end_date": "2025-11-02", "time": null, "patient_name": null, "clarification_needed": false, "missing_fields": []}

Receptionist: "Show me all appointments"
{"intent": "list_appointments", "date": null, "start_date": null, "end_date": null, "time": null, "patient_name": null, "clarification_needed": false, "missing_fields": []}

Receptionist: "Book John Smith at 2pm tomorrow"
{"intent": "book_appointment", "date": "2025-11-01", "time": "14:00", "patient_name": "John Smith", "duration": 30, "clarification_needed": false, "missing_fields": []}

Receptionist: "What appointments do we have tomorrow?"
{"intent": "list_appointments", "date": "2025-11-01", "time": null, "patient_name": null, "clarification_needed": false, "missing_fields": []}

Receptionist: "Book a 1 hour appointment for Sarah at 3pm tomorrow"
{"intent": "book_appointment", "date": "2025-11-01", "time": "15:00", "patient_name": "Sarah", "duration": 60, "clarification_needed": false, "missing_fields": []}

Receptionist: "Cancel Michael's appointment"
{"intent": "cancel_appointment", "date": null, "time": null, "patient_name": "Michael", "duration": 30, "clarification_needed": false, "missing_fields": []}

Receptionist: "I need to book an appointment"
{"intent": "book_appointment", "date": null, "time": null, "patient_name": null, "duration": 30, "clarification_needed": true, "missing_fields": ["date", "time", "patient_name"]}

Receptionist: "What's your name?"
{"intent": "system_info", "date": null, "time": null, "patient_name": null, "clarification_needed": false, "missing_fields": [], "response": "I'm your clinic scheduling assistant. I can help you book appointments, check availability, view your schedule, and manage cancellations. What would you like to do?"}

Receptionist: "What's the weather today?"
{"intent": "out_of_scope", "date": null, "time": null, "patient_name": null, "clarification_needed": false, "missing_fields": [], "response": "I can only help with appointment scheduling. Would you like to book an appointment or check your schedule?"}

DURATION RULES:
- Default duration is ALWAYS 30 minutes
- NEVER include "duration" in missing_fields
- NEVER set clarification_needed=true because of duration
- If user explicitly mentions duration (e.g., "1 hour appointment", "45 minutes"), record it in duration field
- Otherwise always use 30

Return ONLY valid JSON, no explanation."""

        context_part = context if context else "None"
        user_prompt = f"""Previous conversation:
{context_part}

Current receptionist message: "{user_message}"

Parse this into JSON format."""

        max_retries = 2
        for attempt in range(max_retries):
            try:
                print(f"[LLM] Parsing intent (attempt {attempt + 1}/{max_retries})...")
                
                response = requests.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.1,
                        "max_tokens": 500
                    },
                    timeout=45
                )
                
                response.raise_for_status()
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # Remove markdown code blocks if present
                if 'json' in content and '`' in content:
                    start_idx = content.find('{')
                    end_idx = content.rfind('}')
                    if start_idx != -1 and end_idx != -1:
                        content = content[start_idx:end_idx+1]
                
                parsed = json.loads(content)
                
                # Set defaults
                parsed.setdefault('intent', 'book_appointment')
                parsed.setdefault('date', None)
                parsed.setdefault('start_date', None)
                parsed.setdefault('end_date', None)
                parsed.setdefault('time', None)
                parsed.setdefault('patient_name', None)
                parsed.setdefault('duration', 30)
                parsed.setdefault('clarification_needed', False)
                parsed.setdefault('missing_fields', [])
                
                # Force rules for out_of_scope and system_info
                if parsed['intent'] in ['out_of_scope', 'system_info']:
                    parsed['clarification_needed'] = False
                    parsed['missing_fields'] = []
                
                # Remove duration from missing_fields if present
                if 'duration' in parsed['missing_fields']:
                    parsed['missing_fields'].remove('duration')
                    if not parsed['missing_fields']:
                        parsed['clarification_needed'] = False
                
                print(f"[LLM] Intent: {parsed.get('intent')}")
                return parsed
                
            except requests.exceptions.Timeout:
                print(f"[LLM] Timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    continue
                else:
                    print("[LLM] All retry attempts failed")
                    return {
                        'intent': 'error',
                        'error': 'timeout',
                        'clarification_needed': False,
                        'missing_fields': []
                    }
            except Exception as e:
                print(f"[LLM] Error parsing intent: {e}")
                if attempt < max_retries - 1:
                    continue
                return {
                    'intent': 'error',
                    'error': str(e),
                    'clarification_needed': False,
                    'missing_fields': []
                }
    
    def generate_response(self, context):
        """Generate natural response based on context"""
        
        system_prompt = """You are a professional clinic scheduling assistant helping a receptionist.
Generate natural, concise, professional responses. Be helpful and clear.
Format dates as "November 1" not "2025-11-01".
Format times as "2:00 PM" not "14:00"."""

        user_prompt = f"Context: {json.dumps(context)}\nGenerate appropriate response:"
        
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200
                },
                timeout=20
            )
            
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            print(f"[LLM] Error generating response: {e}")
            return "I encountered an error. Could you please repeat that?"


llm_service = LLMService()
