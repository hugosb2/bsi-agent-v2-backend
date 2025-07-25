from flask import Blueprint, request, jsonify
from app.models import agent_model

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/ask', methods=['POST'])
def ask():
    if not request.json or 'question' not in request.json:
        return jsonify({"error": "Requisição inválida. 'question' não encontrada no corpo."}), 400

    user_question = request.json['question']
    history = request.json.get('history', [])

    try:
        answer = agent_model.get_answer_for_question(user_question, history)
        return jsonify({"answer": answer})
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {e}"}), 503