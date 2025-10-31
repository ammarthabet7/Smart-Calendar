📅 Smart Calendar Assistant
Advanced Voice-Enabled AI Scheduling System for Medical Clinics

A production-grade appointment scheduling platform combining state-of-the-art conversational AI, real-time conflict resolution, and seamless voice interaction for healthcare professionals.

🎯 Project Overview
Smart Calendar Assistant is an intelligent appointment scheduling system designed to streamline clinic operations through natural language processing and voice-enabled I/O. The system handles complex scheduling scenarios, intelligent conflict detection, and maintains context across multi-turn conversations—enabling receptionists to manage appointments through natural speech or text.

Key Innovation: LangGraph-powered conversational state machine enables true context-aware appointment management with conflict resolution and business rule enforcement in real-time.

💎 Core Strengths
1. Intelligent Conflict Resolution
Real-time availability checking with instant alternative suggestions

Automatic scheduling optimization around conflicts

Context-aware appointment search and modification

2. Advanced NLP & State Management
Qwen 2.5 72B LLM for nuanced intent parsing and natural responses

LangGraph state machine for robust multi-turn conversation tracking

Maintains conversation history across turns without context loss

Handles ambiguous user inputs with intelligent clarification

3. Seamless Voice Integration
Bidirectional voice I/O (Whisper STT + pyttsx3 TTS)

Natural conversation flow between voice and text input

Professional voice output with proper date/time formatting

Reliable audio recording with silence detection

4. Production-Ready Architecture
Comprehensive error handling and retry logic at all layers

Business rule enforcement (clinic hours, past-date prevention)

Full CRUD operations with context-aware search

Timeout handling and graceful degradation

5. Natural Language Output
LLM-generated responses (not templates)

Intelligent formatting of dates/times for human readability

Context-aware suggestions and confirmations

Professional, conversational tone

🛠️ Technology Stack
Component	Technology	Purpose
LLM Engine	Qwen 2.5 72B (OpenRouter)	Intent parsing, response generation
State Management	LangGraph	Multi-turn conversation handling
Speech-to-Text	OpenAI Whisper	Voice input processing
Text-to-Speech	pyttsx3	Natural voice output
Backend Framework	FastAPI (Python 3.11)	API routing & request handling
Frontend	HTML5/CSS3/Vanilla JS	Responsive web UI
Calendar Logic	Mock Service (In-Memory)	Appointment database & validation
Audio Processing	PyAudio + pygame mixer	Real-time audio capture & playback
🏗️ Architecture Design
text
┌─────────────────────────────────────────┐
│         User Interface (Web)             │
│    ✓ Text Input    ✓ Voice Input        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         FastAPI Router Layer             │
│   • /text endpoint  • /voice endpoint    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│    LangGraph Conversational Agent        │
│  (Intelligent State Machine)             │
├─────────────────────────────────────────┤
│ ✓ Parse Intent Node (LLM)               │
│ ✓ Check Availability Node               │
│ ✓ Book/Cancel/List Nodes                │
│ ✓ Response Generation Node (LLM)        │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┬─────────┐
    │            │            │         │
┌───▼──┐  ┌────▼───┐  ┌────▼──┐  ┌──▼─┐
│ LLM  │  │Calendar│  │  STT  │  │TTS │
│ Svc  │  │  Svc   │  │  Svc  │  │Svc │
└──────┘  └────────┘  └───────┘  └────┘
🚀 Key Capabilities Demonstrated
Appointment Booking
Multi-turn conversation for gathering appointment details

Automatic conflict detection with alternative suggestions

Context-aware patient name retention across turns

Intelligent Conflict Handling
Real-time slot availability verification

Smart suggestion of 3 alternative time slots

Fallback to next available day if current day fully booked

Schedule Management
View appointments by date, date range, or all future appointments

Natural date/time formatting in responses

Context-aware appointment search for cancellations

Business Rule Enforcement
Clinic hours validation (9 AM - 6 PM)

Past-date prevention for new bookings

Clear error messages with helpful guidance

Multi-Turn Conversation
Maintains patient context across multiple conversational turns

Handles follow-ups like "use that time" without re-specification

Conversation history integration for intelligent suggestions

📊 Demo Scenarios
Scenario	Demonstrates	Outcome
Conflict Detection	AI intelligence + context retention	Suggests alternatives automatically
Voice Multi-turn	STT/TTS + conversation flow	Natural booking from voice alone
Schedule Viewing	Data retrieval + natural formatting	Human-readable appointment list
Smart Cancellation	Context-aware search	Cancels using conversation context
Business Validation	Rule enforcement	Rejects out-of-hours requests
⚙️ Quick Setup
bash
# Environment Setup
cd E:\post grad\Smart Calendar
python -m venv venv
venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Configuration
# Add OPENROUTER_API_KEY to .env file

# Launch
python run_server.py
# Access: http://localhost:8000/static/index.html
📁 Project Structure
text
smart-calendar/
├── backend/
│   ├── agent/              # LangGraph nodes & state routing
│   ├── services/           # LLM, Calendar, STT, TTS services
│   ├── routes/             # FastAPI endpoints
│   └── config.py           # Configuration management
├── frontend/
│   └── index.html          # Web UI (responsive design)
└── run_server.py           # Application entry point
✅ Production-Ready Features
✓ Retry logic with exponential backoff
✓ Comprehensive error handling & logging
✓ Multiple time format parsing (2 PM, 14:00, 09:30 AM)
✓ Context retention across conversation turns
✓ Natural language generation (not templates)
✓ Business rule validation & enforcement
✓ Timeout handling with graceful degradation

🎓 Technical Highlights
Conversational State Management: LangGraph ensures conversation context is preserved across multiple turns, enabling the system to understand references like "use that time" without redundant specification.

Intelligent Conflict Resolution: The system performs real-time availability checking and generates contextually appropriate alternatives—not just a generic list.

Multi-Modal I/O: Seamlessly switches between voice and text while maintaining conversation context and business logic.

Production Architecture: Modular service layer with clear separation of concerns, enabling easy scaling and maintenance.