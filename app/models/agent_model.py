import json
import os
from app.services import gemini_service
from datetime import datetime
from zoneinfo import ZoneInfo

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(SCRIPT_DIR)
BACKEND_ROOT = os.path.dirname(APP_DIR)
PDF_CONTENT_PATH = os.path.join(BACKEND_ROOT, "pdf_content.json")
PERSONA_CONFIG_PATH = os.path.join(BACKEND_ROOT, "persona.json")

def load_json_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Arquivo de configuração '{os.path.basename(file_path)}' carregado com sucesso.")
            return data
    except FileNotFoundError:
        print(f"ERRO: O arquivo de configuração '{os.path.basename(file_path)}' não foi encontrado em '{file_path}'.")
        return {}
    except Exception as e:
        print(f"Erro ao carregar o arquivo JSON '{file_path}': {e}")
        return {}

def get_pdf_context_string(data: dict) -> str:
    return "\n\n".join(data.values())

PDF_DATA = load_json_file(PDF_CONTENT_PATH)
PERSONA_CONFIG = load_json_file(PERSONA_CONFIG_PATH)

PDF_CONTEXT = get_pdf_context_string(PDF_DATA)
PERSONA_PROMPT_TEMPLATE = PERSONA_CONFIG.get("persona_prompt", "")
NO_ANSWER_RESPONSE = PERSONA_CONFIG.get("no_answer_response", "Não encontrei a informação.")

def get_answer_for_question(user_question: str, history: list = None) -> str:
    if not PDF_CONTEXT:
        raise ValueError("O contexto dos PDFs não está carregado no servidor.")
    if not PERSONA_PROMPT_TEMPLATE:
        raise ValueError("A configuração da persona não foi carregada.")

    tz = ZoneInfo("America/Sao_Paulo")
    now = datetime.now(tz)
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    data_atual_formatada = f"{dias_semana[now.weekday()]}, {now.day} de {meses[now.month - 1]} de {now.year}."

    persona_prompt = PERSONA_PROMPT_TEMPLATE.replace("{data_atual}", data_atual_formatada)

    conversation_history = ""
    if history:
        for message in history:
            sender = message.get('sender')
            text = message.get('text', '')
            role = "Usuário" if sender == 'user' else "Lívia"
            conversation_history += f"{role}: {text}\n"

    prompt = f"""
    {persona_prompt}

    --- CONTEXTO PARA SUA BASE DE CONHECIMENTO ---
    {PDF_CONTEXT}
    --- FIM DO CONTEXTO ---

    --- HISTÓRICO DA CONVERSA ATUAL ---
    {conversation_history}
    --- FIM DO HISTÓRICO ---

    Com base em todo o seu conhecimento, responda à seguinte pergunta. Se a resposta não estiver no seu conhecimento, diga exatamente: "{NO_ANSWER_RESPONSE}"

    PERGUNTA DO USUÁRIO: "{user_question}"
    """

    return gemini_service.get_ai_response(prompt)