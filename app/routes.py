from flask import Blueprint, render_template, request, jsonify
from app.services.llm_service import get_ai_response #TODO: AI Service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_ai_response(user_input) 
    return jsonify({'response': response})