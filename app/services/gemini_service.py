import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def get_ai_response(prompt: str) -> str:
    
    if not GEMINI_API_KEY:
        raise ValueError("A chave da API do Gemini não está configurada no servidor.")

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    api_response = response.json()

    if 'candidates' in api_response and api_response['candidates']:
        candidate = api_response['candidates'][0]
        if 'content' in candidate and 'parts' in candidate['content'] and candidate['content']['parts']:
            return candidate['content']['parts'][0]['text']

    raise ValueError("Resposta da IA vazia ou em formato inesperado.")
