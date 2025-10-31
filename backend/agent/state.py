from typing import TypedDict, List, Optional, Dict, Any

class ConversationState(TypedDict):
    """State maintained across conversation turns"""
    
    # User input
    user_message: str
    
    # Intent parsing
    intent: Optional[str]
    date: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    time: Optional[str]
    patient_name: Optional[str]
    duration: int
    
    # Calendar data
    appointments: List[Dict[str, Any]]
    available: bool
    
    # Response generation
    agent_response: str
    
    # Conversation management
    conversation_history: List[Dict[str, str]]
    clarification_needed: bool
    missing_fields: List[str]
    
    # Error handling
    error: Optional[str]
    retry_count: int
