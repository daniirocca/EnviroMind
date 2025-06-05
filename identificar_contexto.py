import anthropic
import dotenv
import os
from helpers import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
dados_ambientais_eletroquimicos = carrega('./dados/dados_ambientais_eletroquimicos.txt')
politicas_e_normativas = carrega('./dados/politicas_e_normativas.txt')

def identificar_contexto(prompt):
    prompt_do_sistema = f"""
    O GPT-Enviro possui dois documentos principais que detalham diferentes aspectos do monitoramento ambiental de metais tóxicos:

    # Documento 1 - Dados Ambientais e Eletroquímicos:
    "{dados_ambientais_eletroquimicos}"

    # Documento 2 - Políticas e Normativas Ambientais:
    "{politicas_e_normativas}"

    Avalie o prompt do usuário e retorne o documento mais indicado para ser usado como base na resposta.
    Retorne 'dados' se for o Documento 1, ou 'politicas' se for o Documento 2.
    """
     
    prompt_do_usuario = prompt

    try:
        mensagem = cliente.messages.create(
            model=modelo,
            max_tokens=4000,
            temperature=0,
            system=prompt_do_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_do_usuario
                        }
                    ]
                }
            ]
        )
        resposta = mensagem.content[0].text.lower()
        return resposta
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def selecionar_documento(resposta):
    if "politicas" in resposta:
        return dados_ambientais_eletroquimicos + '\n' + politicas_e_normativas
    else:
        return dados_ambientais_eletroquimicos