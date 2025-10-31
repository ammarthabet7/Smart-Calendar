# Smart Calendar Assistant

**Advanced Voice-Enabled AI Scheduling System for Medical Clinics**

A production-grade appointment scheduling platform combining conversational AI, real-time conflict resolution, and seamless voice interaction for healthcare professionals.

---

## 🎯 Overview

Smart Calendar Assistant streamlines clinic operations through natural language processing and voice-enabled I/O. The system handles complex scheduling scenarios, intelligent conflict detection, and maintains context across multi-turn conversations—enabling receptionists to manage appointments through natural speech or text.

**Key Innovation:** LangGraph-powered conversational state machine enables true context-aware appointment management with conflict resolution in real-time.

---

## 💎 Core Strengths

### 1. Intelligent Conflict Resolution
- Real-time availability checking with instant alternative suggestions
- Automatic scheduling optimization around conflicts
- Context-aware appointment search and modification

### 2. Advanced NLP & State Management
- Qwen 2.5 72B LLM for nuanced intent parsing and natural responses
- LangGraph state machine for robust multi-turn conversation tracking
- Maintains conversation history without context loss
- Handles ambiguous inputs with intelligent clarification

### 3. Seamless Voice Integration
- Bidirectional voice I/O (Whisper STT + pyttsx3 TTS)
- Natural conversation flow between voice and text
- Professional voice output with smart formatting

### 4. Production-Ready Architecture
- Comprehensive error handling at all layers
- Business rule enforcement (clinic hours, past-date prevention)
- Full CRUD operations with context-aware search
- Timeout handling and graceful degradation

### 5. Natural Language Output
- LLM-generated responses (not templates)
- Intelligent date/time formatting
- Context-aware suggestions
- Professional, conversational tone

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM Engine | Qwen 2.5 72B (OpenRouter) |
| State Management | LangGraph |
| Speech-to-Text | OpenAI Whisper |
| Text-to-Speech | pyttsx3 |
| Backend | FastAPI (Python 3.11) |
| Frontend | HTML5/CSS3/Vanilla JS |
| Calendar | Mock Service (In-Memory) |
| Audio | PyAudio + pygame mixer |

---


## 💡 Key Features

**Appointment Booking**
- Multi-turn conversation for gathering details
- Automatic conflict detection with alternatives
- Context-aware patient name retention

**Schedule Management**
- View by date, date range, or all future appointments
- Natural date/time formatting
- Context-aware search for cancellations

**Business Rules**
- Clinic hours validation (9 AM - 6 PM)
- Past-date prevention
- Clear error messages with guidance


---

## 🚀 Future Roadmap

### ElevenLabs Text-to-Speech Integration
Replace pyttsx3 with ElevenLabs API for:
- Ultra-realistic voice synthesis across 32+ languages
- Professional voice cloning for clinic branding
- Real-time streaming with <75ms latency

### Production Calendar APIs
Extend mock service with:
- **Google Calendar API** - Seamless EHR integration
- Real-time multi-user synchronization

### Enhanced Speech Recognition
Upgrade Whisper deployment with:
- Larger model variants for medical terminology
- Custom fine-tuning on clinic vocabulary


---

## 📊 Demo Scenarios

| Scenario | Demonstrates |
|----------|--------------|
| Conflict Detection | AI intelligence + alternatives |
| Voice Multi-turn | STT/TTS + context retention |
| Schedule Viewing | Data retrieval + natural formatting |
| Smart Cancellation | Context-aware search |
| Business Validation | Rule enforcement |



---

## ✅ Production Features

✓ Retry logic with timeout handling  
✓ Multiple time format parsing  
✓ Context retention across turns  
✓ Natural language generation  
✓ Business rule validation  

---

**Status:** Production-ready | **Demo:** 3:40 min | **Tech Level:** Advanced
