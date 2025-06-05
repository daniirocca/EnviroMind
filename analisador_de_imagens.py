import anthropic
import dotenv
import os
from helpers import *
import re

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"

def analisar_imagem(caminho_imagem):
    prompt_do_sistema = f"""
    Você é um assistente especializado em análise de voltamogramas anódicos por redissolução (ASV) para detecção de metais tóxicos em corpos hídricos.

    Ao receber a imagem de um voltamograma (corrente vs. potencial), siga estes passos:

    1. Analise a curva e identifique todos os picos relevantes, informando o potencial (V) e a corrente de pico (µA) de cada um.
    2. Para cada pico, sugira qual metal pode estar associado, com base no potencial padrão de oxidação/redução.
    3. **Estime a concentração do metal correspondente ao pico principal**. Para isso, use a relação linear entre corrente de pico (µA) e concentração (µg/L) típica de curvas de calibração ASV. Se necessário, assuma que a curva de calibração é do tipo: corrente = a * concentração + b, e explique como chegou ao valor.
    4. Compare a concentração estimada com os limites legais (CONAMA 357/2005, OMS ou CETESB) e informe explicitamente se está acima ou abaixo do limite, citando o valor do limite.
    5. Ao final, apresente de forma clara:
        - O metal identificado
        - O valor da corrente de pico (µA)
        - A concentração estimada (µg/L)
        - O limite legal correspondente e se está acima ou abaixo

    Se não for possível estimar a concentração, explique o motivo.

    Responda de forma objetiva, técnica e cite sempre os valores numéricos.
    """
    imagem_base64 = encodar_imagem(caminho_imagem)
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
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": imagem_base64,
                            },
                        },
                    ]
                }
            ]
        )
        resposta = mensagem.content[0].text
        metais_suportados = ['pb', 'cd', 'hg', 'as']

        nomes_metal = {
            'chumbo': 'pb', 'lead': 'pb',
            'cádmio': 'cd', 'cadmio': 'cd', 'cadmium': 'cd',
            'mercúrio': 'hg', 'mercurio': 'hg', 'mercury': 'hg',
            'arsênio': 'as', 'arsenio': 'as', 'arsenic': 'as'
        }

        padrao_metais = r'(' + '|'.join(metais_suportados + list(nomes_metal.keys())) + r')[^\d]*(\d+[\.,]?\d*)\s*µA'
        match = re.search(padrao_metais, resposta, re.IGNORECASE)
        if match:
            metal_bruto = match.group(1).lower()
            metal = nomes_metal.get(metal_bruto, metal_bruto)
            if metal in metais_suportados:
                corrente_pico = float(match.group(2).replace(',', '.'))
                concs, corrs = carregar_curva_calibracao(metal)
                conc_estim = estimar_concentracao(corrs, concs, corrente_pico)
                if conc_estim:
                    resposta += f"\n\nConcentração estimada para {metal.upper()}: {conc_estim:.2f} µg/L (usando curva de calibração)."
            else:
                resposta += "\n\nMetal identificado não possui curva de calibração cadastrada."
        return resposta
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")