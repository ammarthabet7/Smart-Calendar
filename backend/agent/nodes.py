from backend.agent.state import ConversationState
from backend.services.llm_service import llm_service
from backend.services.calendar_service import calendar_service
from datetime import datetime, timedelta, time
from backend.config import settings


def parse_intent_node(state: ConversationState) -> ConversationState:
    """Node 1: Parse user input into structured intent"""
    print(f"\n[NODE: PARSE INTENT] Processing: '{state['user_message']}'")
    
    if not state.get('user_message') or len(state['user_message'].strip()) < 2:
        state['intent'] = 'error'
        state['error'] = 'empty_input'
        state['agent_response'] = "I didn't catch that. Could you please speak again?"
        return state
    
    intent_data = llm_service.parse_intent(
        state['user_message'],
        state.get('conversation_history', [])
    )
    
    state['intent'] = intent_data.get('intent')
    state['date'] = intent_data.get('date')
    state['time'] = intent_data.get('time')
    state['patient_name'] = intent_data.get('patient_name')
    state['duration'] = intent_data.get('duration', 30)
    state['clarification_needed'] = intent_data.get('clarification_needed', False)
    state['missing_fields'] = intent_data.get('missing_fields', [])
    
    if 'duration' in state['missing_fields']:
        state['missing_fields'].remove('duration')
        if not state['missing_fields']:
            state['clarification_needed'] = False
    
    if state['intent'] in ['out_of_scope', 'system_info']:
        state['clarification_needed'] = False
        state['agent_response'] = intent_data.get('response', 
            "I'm your clinic scheduling assistant. I can help you book appointments, check availability, or view your schedule. What would you like to do?")
    
    print(f"[NODE: PARSE INTENT] Intent: {state['intent']}, Date: {state.get('date')}, Time: {state.get('time')}")
    print(f"[NODE: PARSE INTENT] Clarification needed: {state['clarification_needed']}, Missing: {state['missing_fields']}")
    
    return state


def list_appointments_node(state: ConversationState) -> ConversationState:
    """List appointments node with date range support and LLM-generated responses"""
    date = state.get('date')
    start_date = state.get('start_date')
    end_date = state.get('end_date')
    
    print(f"[NODE: LIST APPOINTMENTS] Date: {date}, Range: {start_date} to {end_date}")
    
    if start_date and end_date:
        print(f"[NODE: LIST APPOINTMENTS] Listing appointments from {start_date} to {end_date}")
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            state['agent_response'] = "I couldn't understand that date range. Please provide valid dates."
            return state
        
        all_appointments = []
        current = start
        while current <= end:
            date_str = current.strftime('%Y-%m-%d')
            day_appointments = calendar_service.get_appointments(date_str)
            
            for apt in day_appointments:
                date_obj = datetime.strptime(apt['date'], '%Y-%m-%d')
                time_obj = datetime.strptime(apt['time'], '%H:%M')
                all_appointments.append({
                    'patient': apt['patient_name'],
                    'date': date_obj.strftime('%B %d'),
                    'time': time_obj.strftime('%I:%M %p').lstrip('0'),
                    'day_of_week': date_obj.strftime('%A')
                })
            
            current += timedelta(days=1)
        
        state['appointments'] = all_appointments
        
        if not all_appointments:
            context = {
                'intent': 'list_appointments',
                'result': 'no_appointments',
                'start_date': start.strftime('%B %d'),
                'end_date': end.strftime('%B %d')
            }
        else:
            context = {
                'intent': 'list_appointments',
                'result': 'found_appointments_range',
                'count': len(all_appointments),
                'appointments': all_appointments,
                'start_date': start.strftime('%B %d'),
                'end_date': end.strftime('%B %d')
            }
        
        state['agent_response'] = llm_service.generate_response(context)
        
    elif start_date and not end_date:
        print(f"[NODE: LIST APPOINTMENTS] Listing appointments from {start_date} onwards (7 days)")
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = start + timedelta(days=7)
        except ValueError:
            state['agent_response'] = "I couldn't understand that date. Please provide a valid date."
            return state
        
        all_appointments = []
        current = start
        while current <= end:
            date_str = current.strftime('%Y-%m-%d')
            day_appointments = calendar_service.get_appointments(date_str)
            
            for apt in day_appointments:
                date_obj = datetime.strptime(apt['date'], '%Y-%m-%d')
                time_obj = datetime.strptime(apt['time'], '%H:%M')
                all_appointments.append({
                    'patient': apt['patient_name'],
                    'date': date_obj.strftime('%B %d'),
                    'time': time_obj.strftime('%I:%M %p').lstrip('0'),
                    'day_of_week': date_obj.strftime('%A')
                })
            
            current += timedelta(days=1)
        
        state['appointments'] = all_appointments
        
        if not all_appointments:
            context = {
                'intent': 'list_appointments',
                'result': 'no_appointments',
                'start_date': start.strftime('%B %d'),
                'future_request': True
            }
        else:
            context = {
                'intent': 'list_appointments',
                'result': 'found_appointments_range',
                'count': len(all_appointments),
                'appointments': all_appointments,
                'start_date': start.strftime('%B %d'),
                'future_request': True
            }
        
        state['agent_response'] = llm_service.generate_response(context)
        
    elif not date and not start_date:
        print(f"[NODE: LIST APPOINTMENTS] Listing all future appointments")
        
        appointments = calendar_service.get_appointments()
        state['appointments'] = appointments
        
        if not appointments:
            context = {
                'intent': 'list_appointments',
                'result': 'no_appointments',
                'all_future': True
            }
        else:
            apt_info = []
            for apt in appointments:
                date_obj = datetime.strptime(apt['date'], '%Y-%m-%d')
                time_obj = datetime.strptime(apt['time'], '%H:%M')
                apt_info.append({
                    'patient': apt['patient_name'],
                    'date': date_obj.strftime('%B %d'),
                    'time': time_obj.strftime('%I:%M %p').lstrip('0'),
                    'day_of_week': date_obj.strftime('%A')
                })
            
            context = {
                'intent': 'list_appointments',
                'result': 'found_appointments',
                'count': len(apt_info),
                'appointments': apt_info,
                'all_future': True
            }
        
        state['agent_response'] = llm_service.generate_response(context)
        
    else:
        print(f"[NODE: LIST APPOINTMENTS] Listing appointments for {date}")
        
        appointments = calendar_service.get_appointments(date)
        state['appointments'] = appointments
        
        if not appointments:
            context = {
                'intent': 'list_appointments',
                'date': date,
                'result': 'no_appointments'
            }
        else:
            apt_info = []
            for apt in appointments:
                date_obj = datetime.strptime(apt['date'], '%Y-%m-%d')
                time_obj = datetime.strptime(apt['time'], '%H:%M')
                apt_info.append({
                    'patient': apt['patient_name'],
                    'date': date_obj.strftime('%B %d'),
                    'time': time_obj.strftime('%I:%M %p').lstrip('0')
                })
            
            context = {
                'intent': 'list_appointments',
                'date': date,
                'result': 'found_appointments',
                'count': len(apt_info),
                'appointments': apt_info
            }
        
        state['agent_response'] = llm_service.generate_response(context)
    
    return state


def check_availability_node(state: ConversationState) -> ConversationState:
    """Node 3: Check availability with past date validation"""
    print(f"\n[NODE: CHECK AVAILABILITY] Checking {state.get('date')} at {state.get('time')}")
    
    if not state.get('time'):
        context = {
            'intent': 'check_availability',
            'error': 'missing_time',
            'date': state.get('date')
        }
        state['agent_response'] = llm_service.generate_response(context)
        state['clarification_needed'] = True
        return state
    
    # Validate date is not in the past for booking
    if state.get('intent') == 'book_appointment':
        try:
            date_obj = datetime.strptime(state['date'], '%Y-%m-%d')
            if date_obj.date() < datetime.now().date():
                context = {
                    'intent': 'book_appointment',
                    'error': 'past_date',
                    'date': state['date']
                }
                state['agent_response'] = llm_service.generate_response(context)
                state['available'] = False
                return state
        except ValueError:
            pass
    
    # Check availability
    result = calendar_service.check_availability(state['date'], state['time'])
    state['available'] = result.get('available', False)
    
    # Outside business hours
    if result.get('reason') == 'outside_hours':
        context = {
            'intent': state.get('intent'),
            'error': 'outside_hours',
            'date': state['date'],
            'time': state['time'],
            'clinic_hours': f"{settings.CLINIC_HOURS_START} to {settings.CLINIC_HOURS_END}"
        }
        state['agent_response'] = llm_service.generate_response(context)
        state['available'] = False
    
    # If slot is available and intent is check_availability, generate response
    elif state['available'] and state.get('intent') == 'check_availability':
        date_obj = datetime.strptime(state['date'], '%Y-%m-%d')
        
        # SAFELY PARSE TIME - handle AM/PM if present
        time_str = state['time']
        if 'AM' in time_str.upper() or 'PM' in time_str.upper():
            time_str = calendar_service._parse_time_to_24h(time_str)
        
        time_obj = datetime.strptime(time_str, '%H:%M')
        formatted_date = date_obj.strftime('%B %d')
        formatted_time = time_obj.strftime('%I:%M %p').lstrip('0')
        
        context = {
            'intent': 'check_availability',
            'result': 'available',
            'date': formatted_date,
            'time': formatted_time
        }
        state['agent_response'] = llm_service.generate_response(context)
    
    # Slot already booked - find alternatives
    elif not state['available']:
        date_obj = datetime.strptime(state['date'], '%Y-%m-%d')
        day_appointments = calendar_service.get_appointments(state['date'])
        booked_times = [apt['time'] for apt in day_appointments]
        
        available_slots = []
        current_time = datetime.strptime(settings.CLINIC_HOURS_START, '%H:%M').time()
        end_time = datetime.strptime(settings.CLINIC_HOURS_END, '%H:%M').time()
        
        while current_time < end_time:
            time_str = current_time.strftime('%H:%M')
            if time_str not in booked_times:
                formatted_time = datetime.strptime(time_str, '%H:%M').strftime('%I:%M %p').lstrip('0')
                available_slots.append({'time': time_str, 'formatted': formatted_time})
            
            temp_dt = datetime.combine(date_obj, current_time) + timedelta(minutes=30)
            current_time = temp_dt.time()
        
        # If no slots available that day, check next day
        if not available_slots:
            next_day = date_obj + timedelta(days=1)
            next_day_str = next_day.strftime('%Y-%m-%d')
            next_day_appointments = calendar_service.get_appointments(next_day_str)
            next_booked = [apt['time'] for apt in next_day_appointments]
            
            current_time = datetime.strptime(settings.CLINIC_HOURS_START, '%H:%M').time()
            while current_time < end_time:
                time_str = current_time.strftime('%H:%M')
                if time_str not in next_booked:
                    formatted_time = datetime.strptime(time_str, '%H:%M').strftime('%I:%M %p').lstrip('0')
                    formatted_date = next_day.strftime('%B %d')
                    available_slots.append({
                        'time': time_str,
                        'formatted': formatted_time,
                        'date': next_day_str,
                        'formatted_date': formatted_date
                    })
                    break
                temp_dt = datetime.combine(next_day, current_time) + timedelta(minutes=30)
                current_time = temp_dt.time()
        
        # Format requested time safely
        requested_time_str = state['time']
        if 'AM' in requested_time_str.upper() or 'PM' in requested_time_str.upper():
            requested_time_str = calendar_service._parse_time_to_24h(requested_time_str)
        
        requested_time = datetime.strptime(requested_time_str, '%H:%M').strftime('%I:%M %p').lstrip('0')
        requested_date = date_obj.strftime('%B %d')
        
        context = {
            'intent': state.get('intent'),
            'error': 'slot_taken',
            'requested_date': requested_date,
            'requested_time': requested_time,
            'available_slots': available_slots[:3],
            'booked_with': result.get('message', '')
        }
        state['agent_response'] = llm_service.generate_response(context)
    
    print(f"[NODE: CHECK AVAILABILITY] Available: {state['available']}")
    return state


def book_appointment_node(state: ConversationState) -> ConversationState:
    """Book appointment node with LLM-generated confirmation"""
    date = state['date']
    time = state['time']
    patient_name = state['patient_name']
    duration = state.get('duration', 30)
    
    print(f"[NODE: BOOK APPOINTMENT] Booking for {patient_name} on {date} at {time}")
    
    result = calendar_service.book_appointment(date, time, patient_name, duration)
    
    # Format date and time for LLM context
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    # SAFELY PARSE TIME - handle AM/PM if present
    time_str = time
    if 'AM' in time_str.upper() or 'PM' in time_str.upper():
        time_str = calendar_service._parse_time_to_24h(time_str)
    
    time_obj = datetime.strptime(time_str, '%H:%M')
    formatted_date = date_obj.strftime('%B %d')
    formatted_time = time_obj.strftime('%I:%M %p').lstrip('0')
    
    if result['success']:
        context = {
            'intent': 'book_appointment',
            'result': 'success',
            'patient_name': patient_name,
            'date': formatted_date,
            'time': formatted_time,
            'duration': duration
        }
        state['agent_response'] = llm_service.generate_response(context)
    else:
        context = {
            'intent': 'book_appointment',
            'result': 'failure',
            'error_message': result.get('message', 'Could not book appointment')
        }
        state['agent_response'] = llm_service.generate_response(context)
    
    return state


def cancel_appointment_node(state: ConversationState) -> ConversationState:
    """Cancel appointment node with LLM-generated confirmation"""
    date = state.get('date')
    time = state.get('time')
    patient_name = state.get('patient_name')
    
    print(f"[NODE: CANCEL APPOINTMENT] Date: {date}, Time: {time}, Patient: {patient_name}")
    
    if not date and not patient_name:
        context = {
            'intent': 'cancel_appointment',
            'error': 'missing_info',
            'message': 'Please provide the appointment date or patient name to cancel'
        }
        state['agent_response'] = llm_service.generate_response(context)
        return state
    
    result = calendar_service.cancel_appointment(date, time, patient_name)
    
    if result['success']:
        apt = result['appointment']
        date_obj = datetime.strptime(apt['date'], '%Y-%m-%d')
        time_obj = datetime.strptime(apt['time'], '%H:%M')
        formatted_date = date_obj.strftime('%B %d')
        formatted_time = time_obj.strftime('%I:%M %p').lstrip('0')
        
        context = {
            'intent': 'cancel_appointment',
            'result': 'success',
            'patient_name': apt['patient_name'],
            'date': formatted_date,
            'time': formatted_time
        }
        state['agent_response'] = llm_service.generate_response(context)
    else:
        context = {
            'intent': 'cancel_appointment',
            'result': 'not_found',
            'error_message': result.get('message', 'Appointment not found'),
            'date': date,
            'time': time,
            'patient_name': patient_name
        }
        state['agent_response'] = llm_service.generate_response(context)
    
    return state


def generate_response_node(state: ConversationState) -> ConversationState:
    """Generate natural language response using LLM"""
    
    print(f"\n[NODE: GENERATE RESPONSE] Intent: {state.get('intent')}, Pre-set response: {bool(state.get('agent_response'))}")
    
    if state.get('agent_response'):
        print(f"[NODE: GENERATE RESPONSE] Using pre-set response")
        return state
    
    if state.get('clarification_needed'):
        missing = state.get('missing_fields', [])
        intent = state.get('intent')
        
        print(f"[NODE: GENERATE RESPONSE] Generating clarification for missing: {missing}")
        
        context = {
            'intent': intent,
            'clarification_needed': True,
            'missing_fields': missing,
            'has_date': bool(state.get('date')),
            'has_time': bool(state.get('time')),
            'has_patient': bool(state.get('patient_name')),
            'date': state.get('date'),
            'time': state.get('time'),
            'patient_name': state.get('patient_name')
        }
        
        state['agent_response'] = llm_service.generate_response(context)
    
    if not state.get('agent_response'):
        print(f"[NODE: GENERATE RESPONSE] No response yet, using LLM fallback")
        context = {
            'intent': state.get('intent'),
            'clarification_needed': state.get('clarification_needed'),
            'missing_fields': state.get('missing_fields', [])
        }
        state['agent_response'] = llm_service.generate_response(context)
    
    print(f"[NODE: GENERATE RESPONSE] Final response: '{state['agent_response']}'")
    return state
