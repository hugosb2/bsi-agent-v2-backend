import os
import fitz
import json
import unicodedata

def extract_text_from_pdfs(pdf_folder_path, output_json_path):
    pdf_contents = {}
    print(f"Procurando por PDFs em: {pdf_folder_path}")

    if not os.path.isdir(pdf_folder_path):
        print(f"Erro: A pasta '{pdf_folder_path}' não foi encontrada.")
        print("Por favor, certifique-se de que a pasta 'pdfs' existe no mesmo diretório que este script.")
        return

    for filename in os.listdir(pdf_folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(pdf_folder_path, filename)
            print(f"Processando arquivo: {filename}...")
            try:
                doc = fitz.open(file_path)
                full_text = ""
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    full_text += page.get_text("text")
                
                normalized_text = unicodedata.normalize('NFKD', full_text).encode('ascii', 'ignore').decode('utf-8')
                pdf_contents[filename] = normalized_text
                print(f"Texto extraído de {filename} com sucesso.")

            except Exception as e:
                print(f"Não foi possível processar o arquivo {filename}. Erro: {e}")

    if not pdf_contents:
        print("Nenhum arquivo PDF foi processado. O arquivo JSON não será criado.")
        return

    try:
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(pdf_contents, json_file, ensure_ascii=False, indent=4)
        print(f"\nExtração concluída! Conteúdo salvo em: {output_json_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_folder = os.path.join(script_dir, "pdfs")
    json_output_file = os.path.join(script_dir, "pdf_content.json")
    
    extract_text_from_pdfs(pdf_folder, json_output_file)