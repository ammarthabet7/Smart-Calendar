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

## 🏗️ Architecture

