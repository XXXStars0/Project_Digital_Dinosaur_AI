import re  
from flask import Blueprint, render_template, request, jsonify
from app.services.llm_service import get_ai_response 
from app.services.game_state import current_game_state 
from app.services.memory_service import remember, recall

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', initial_state=current_game_state.get_state())

@main_bp.route('/api/interact', methods=['POST'])
def interact():
    data = request.json
    user_input = data.get('message', "")
    action_type = data.get('action') 

    current_stats, event_desc = current_game_state.handle_action(action_type)

    relevant_memories = ""
    if user_input:
        relevant_memories = recall(user_input)
        print(f"--- [RAG Debug] Found Memories: ---\n{relevant_memories}\n---")

    raw_response = get_ai_response(user_input, current_stats, event_desc, relevant_memories) 

    if user_input:
        remember(f"User said: {user_input}")

    final_response_text = raw_response
    
    # Parse NEW_NAME marker
    match = re.search(r'\[NEW_NAME:\s*(.*?)\]', raw_response)
    if match:
        new_name = match.group(1)
        current_game_state.update_name(new_name)
        final_response_text = final_response_text.replace(match.group(0), "").strip()
    
    # Parse STAT_CHANGE marker (for chat-based stat changes)
    stat_match = re.search(r'\[STAT_CHANGE:\s*(.*?)\]', raw_response)
    if stat_match:
        stat_string = stat_match.group(1)
        stat_changes = {}
        
        # Parse stat changes like "hunger:+25, mood:+5, affinity:+2"
        for stat_pair in stat_string.split(','):
            stat_pair = stat_pair.strip()
            if ':' in stat_pair:
                stat_name, stat_value = stat_pair.split(':', 1)
                stat_name = stat_name.strip()
                try:
                    stat_value = int(stat_value.strip())
                    stat_changes[stat_name] = stat_value
                except ValueError:
                    pass
        
        # Apply stat changes if any were parsed
        if stat_changes:
            current_game_state.apply_stat_changes(stat_changes)
            # Remove the marker from response
            final_response_text = final_response_text.replace(stat_match.group(0), "").strip()

    return jsonify({
        'response': final_response_text,
        'stats': current_game_state.get_state() 
    })