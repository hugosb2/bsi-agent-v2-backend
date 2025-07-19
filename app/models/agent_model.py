import json
import os
from app.services import gemini_service


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

# Extrai as informações necessárias das configurações
PDF_CONTEXT = get_pdf_context_string(PDF_DATA)
PERSONA_PROMPT = PERSONA_CONFIG.get("persona_prompt", "")
NO_ANSWER_RESPONSE = PERSONA_CONFIG.get("no_answer_response", "Não encontrei a informação.")

def get_answer_for_question(user_question: str) -> str:

    if not PDF_CONTEXT:
        raise ValueError("O contexto dos PDFs não está carregado no servidor.")
    if not PERSONA_PROMPT:
        raise ValueError("A configuração da persona não foi carregada.")

    prompt = f"""
    {PERSONA_PROMPT}

    --- CONTEXTO PARA SUA BASE DE CONHECIMENTO ---
    {PDF_CONTEXT}
    --- FIM DO CONTEXTO ---

    Com base no seu conhecimento, responda à seguinte pergunta. Se a resposta não estiver no seu conhecimento, diga exatamente: "{NO_ANSWER_RESPONSE}"

    PERGUNTA DO USUÁRIO: "{user_question}"
    """

    return gemini_service.get_ai_response(prompt)
