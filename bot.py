import anthropic
import dotenv
import os
from helpers import *
from identificar_contexto import *
from analisador_de_imagens import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
import re
import shutil
import numpy as np


dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"

def gerar_grafico_potencial_corrente(dados_texto):
    potenciais = []
    correntes = []
    dados_texto = dados_texto.replace('\n', ' ')
    pares = re.findall(r'(-?\d+[\.,]?\d*)\s*[,;\s]\s*(-?\d+[\.,]?\d*)', dados_texto)
    for par in pares:
        try:
            potenciais.append(float(par[0].replace(',', '.')))
            correntes.append(float(par[1].replace(',', '.')))
        except ValueError:
            continue
    if potenciais and correntes:
        fig, ax = plt.subplots()
        ax.plot(potenciais, correntes, marker='o')
        ax.set_xlabel('Potencial (V)')
        ax.set_ylabel('Corrente (µA)')
        ax.set_title('Curva Voltamétrica')
        import uuid
        nome_arquivo = f"voltamograma_{uuid.uuid4().hex}.jpg"
        caminho_arquivo = os.path.join("static", "fotos", nome_arquivo)
        plt.savefig(caminho_arquivo, format='jpg')
        plt.close(fig)
        return f"static/fotos/{nome_arquivo}"
    return None

def contem_dados_potencial_corrente(texto):
    linhas = texto.strip().split('\n')
    padrao = re.compile(r'^-?\d+[\.,]?\d*\s*[,;\t ]\s*-?\d+[\.,]?\d*')
    for linha in linhas:
        if padrao.match(linha.strip()):
            return True
    return False

def bot(prompt, historico, caminho_da_imagem):
    contexto = identificar_contexto(prompt)
    documento_contexto = selecionar_documento(contexto)
    prompt_do_sistema = f"""
    Você é o **EnviroAI**, um agente de inteligência artificial especializado na **análise e interpretação de dados eletroquímicos voltamétricos (ASV)** para o **monitoramento ambiental de metais tóxicos em corpos hídricos**.  
    Você deve **responder exclusivamente com base em dados fornecidos pelo sistema/aplicativo**, sem extrapolar ou inventar informações não presentes.  
    Sua resposta deve considerar **tanto o contexto técnico quanto o histórico da conversa anterior** para garantir coerência e continuidade analítica.

    ## Diretrizes:

    - Use apenas os dados disponíveis no aplicativo ou sensores informados.
    - Utilize o contexto técnico descrito abaixo para fundamentar as análises.
    - Leve em conta o histórico de interações para manter consistência nas respostas.
    - Todas as respostas devem seguir princípios científicos e regulamentações ambientais.

    ---

    ### Contexto Técnico
    {documento_contexto}
    ---

    ### Histórico de Conversa
    {historico}

    """
    analise_da_imagem = ''
    imagem_gerada = False
    caminho_imagem_estatica = None

    def extrair_dados_potencial_corrente(texto):
        import re
        potenciais = []
        correntes = []
        pares = re.findall(r'(-?\d+[\.,]?\d*)\s*[,;\s]\s*(-?\d+[\.,]?\d*)', texto)
        for pot, corr in pares:
            potenciais.append(float(pot.replace(',', '.')))
            correntes.append(float(corr.replace(',', '.')))
        return np.array(potenciais), np.array(correntes)

    def identificar_pico(potenciais, correntes):
        idx_pico = np.argmax(correntes)
        return potenciais[idx_pico], correntes[idx_pico]

    if contem_dados_potencial_corrente(prompt):
        potenciais, correntes = extrair_dados_potencial_corrente(prompt)
        pico_pot, pico_corr = identificar_pico(potenciais, correntes)
        metal = 'pb'
        curva_concs, curva_corrs = carregar_curva_calibracao(metal)
        conc_estim = estimar_concentracao(curva_concs, curva_corrs, pico_corr)
        analise_da_imagem = (
            f"\nAnálise automática dos dados fornecidos:\n"
            f"Pico principal em {pico_pot:.2f} V, corrente de pico {pico_corr:.2f} µA.\n"
            f"Metal identificado: Pb (chumbo).\n"
            f"Concentração estimada: {conc_estim:.2f} µg/L.\n"
        )
        caminho_imagem_estatica = gerar_grafico_potencial_corrente(prompt)


    if caminho_da_imagem is not None:
        analise_da_imagem = analisar_imagem(caminho_da_imagem)
        analise_da_imagem += '. Na resposta final, apresente os detalhes da descrição da imagem'
        if imagem_gerada:
            os.remove(caminho_da_imagem)
        caminho_da_imagem = None

    prompt_do_usuario = prompt + analise_da_imagem + "\n\nResponda apenas com a análise técnica, sem agradecimentos, introduções ou repetições do enunciado."

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
        resposta = mensagem.content[0].text
        return resposta, caminho_da_imagem, caminho_imagem_estatica
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")