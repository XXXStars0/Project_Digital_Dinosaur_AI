import re  
from flask import Blueprint, render_template, request, jsonify
from app.services.llm_service import get_ai_response 
from app.services.game_state import current_game_state 

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', initial_state=current_game_state.get_state())

@main_bp.route('/api/interact', methods=['POST'])
def interact():
    data = request.json
    user_input = data.get('message', "")
    action_type = data.get('action') # 'feed', 'pet', 'chat', 'sleep'

    current_stats, event_desc = current_game_state.handle_action(action_type)
    raw_response = get_ai_response(user_input, current_stats, event_desc) 
    final_response_text = raw_response
    
    match = re.search(r'\[NEW_NAME:\s*(.*?)\]', raw_response)
    
    if match:
        new_name = match.group(1) 
        
        current_game_state.update_name(new_name)
        
        final_response_text = raw_response.replace(match.group(0), "").strip()

    return jsonify({
        'response': final_response_text,
        'stats': current_game_state.get_state() 
    })