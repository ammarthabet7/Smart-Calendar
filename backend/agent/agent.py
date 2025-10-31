from langgraph.graph import StateGraph, END
from backend.agent.state import ConversationState
from backend.agent.graph import agent_graph  # ADD THIS LINE IF MISSING
from backend.services.tts_service import tts_service


class AppointmentAgent:
    """Main agent interface for handling conversations"""
    
    def __init__(self):
        self.graph = agent_graph
        self.conversation_history = []  # ADD THIS LINE
        print("[AGENT] Appointment agent initialized")
    
    def process_message(self, user_message: str, conversation_history=None) -> dict:
        """Process a user message and return response"""
        print(f"\n{'='*60}")
        print(f"[AGENT] Processing message: '{user_message}'")
        print(f"{'='*60}")
        
        # Use instance history if none provided
        if conversation_history is None:
            conversation_history = self.conversation_history
        
        # Initialize state
        initial_state: ConversationState = {
            'user_message': user_message,
            'intent': None,
            'date': None,
            'start_date': None,
            'end_date': None,
            'time': None,
            'patient_name': None,
            'duration': 30,
            'appointments': [],
            'available': False,
            'agent_response': '',
            'conversation_history': conversation_history,
            'clarification_needed': False,
            'missing_fields': [],
            'error': None,
            'retry_count': 0
        }
        
        try:
            # Run through graph
            final_state = self.graph.invoke(initial_state)
            
            response = final_state.get('agent_response', 'I apologize, I could not process that request.')
            
            print(f"\n[AGENT] Final response: '{response}'")
            print(f"{'='*60}\n")
            
            # Save to history
            self.conversation_history.append({
                'user': user_message,
                'agent': response
            })
            
            # Keep only last 5 turns
            self.conversation_history = self.conversation_history[-5:]
            
            # Speak response using TTS
            tts_service.speak(response)
            
            return {
                'success': True,
                'response': response,
                'intent': final_state.get('intent'),
                'state': final_state
            }
            
        except Exception as e:
            print(f"[AGENT] Error processing message: {e}")
            error_response = "I encountered an error. Could you please repeat that?"
            
            # Save error to history
            self.conversation_history.append({
                'user': user_message,
                'agent': error_response
            })
            
            # Speak error response
            tts_service.speak(error_response)
        
        return {
            'success': False,
            'response': error_response,
            'intent': None,
            'error': str(e)
        }

            
       
# Create singleton instance
appointment_agent = AppointmentAgent()

