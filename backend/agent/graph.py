from langgraph.graph import StateGraph, END
from backend.agent.state import ConversationState
from backend.agent.nodes import (
    parse_intent_node,
    list_appointments_node,
    check_availability_node,
    book_appointment_node,
    cancel_appointment_node,
    generate_response_node
)


def route_after_intent(state: ConversationState) -> str:
    """Router: Decide next action based on parsed intent"""
    intent = state.get('intent')
    
    print(f"[ROUTER: INTENT] Routing intent: {intent}")
    
    # Edge case handling
    if intent == 'error' or intent == 'out_of_scope' or intent == 'system_info':
        return 'respond'
    
    if state.get('clarification_needed'):
        return 'respond'
    
    # Route based on intent
    if intent == 'list_appointments':
        return 'list'
    elif intent == 'book_appointment':
        return 'check_availability'
    elif intent == 'check_availability':
        return 'check_availability'
    elif intent == 'cancel_appointment':
        return 'cancel'
    else:
        return 'respond'


def route_after_availability(state: ConversationState) -> str:
    """Router: Decide if we proceed to booking or respond"""
    intent = state.get('intent')
    available = state.get('available')
    
    print(f"[ROUTER: AVAILABILITY] Intent: {intent}, Available: {available}")
    
    # Only book if intent is book_appointment AND slot is available
    if intent == 'book_appointment' and available:
        return 'book'
    else:
        return 'respond'


def create_agent_graph():
    """Create the LangGraph state machine"""
    
    # Initialize graph
    workflow = StateGraph(ConversationState)
    
    # Add nodes
    workflow.add_node("parse_intent", parse_intent_node)
    workflow.add_node("list", list_appointments_node)
    workflow.add_node("check_availability", check_availability_node)
    workflow.add_node("book", book_appointment_node)
    workflow.add_node("cancel", cancel_appointment_node)
    workflow.add_node("respond", generate_response_node)
    
    # Set entry point
    workflow.set_entry_point("parse_intent")
    
    # Add conditional routing from parse_intent
    workflow.add_conditional_edges(
        "parse_intent",
        route_after_intent,
        {
            "list": "list",
            "check_availability": "check_availability",
            "cancel": "cancel",
            "respond": "respond"
        }
    )
    
    # List appointments always goes to respond
    workflow.add_edge("list", "respond")
    
    # Cancel always goes to respond
    workflow.add_edge("cancel", "respond")
    
    # Availability check routes to book or respond
    workflow.add_conditional_edges(
        "check_availability",
        route_after_availability,
        {
            "book": "book",
            "respond": "respond"
        }
    )
    
    # Booking always goes to respond
    workflow.add_edge("book", "respond")
    
    # Respond is the end
    workflow.add_edge("respond", END)
    
    # Compile graph
    graph = workflow.compile()
    
    print("[GRAPH] Agent graph compiled successfully")
    return graph


# Create the agent
agent_graph = create_agent_graph()
