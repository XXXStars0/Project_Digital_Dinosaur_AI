from flask import Blueprint, render_template, request, jsonify
# Inport AI service
from app.services.llm_service import get_ai_response 

from app.services.game_state import current_game_state 

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', initial_state=current_game_state.get_state())

@main_bp.route('/api/interact', methods=['POST']) #
def interact():
    data = request.json
    user_input = data.get('message', "")
    action_type = data.get('action') # Action From Frontend


    current_stats, event_desc = current_game_state.handle_action(action_type)

    ai_response = get_ai_response(user_input, current_stats, event_desc) 

    return jsonify({
        'response': ai_response,
        'stats': current_stats 
    })