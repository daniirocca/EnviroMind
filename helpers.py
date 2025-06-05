import base64
import csv
import numpy as np

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def encodar_imagem(caminho_imagem): 
    with open(caminho_imagem, "rb") as arquivo_imagem:
        return base64.b64encode(arquivo_imagem.read()).decode('utf-8')
    
def carregar_curva_calibracao(metal):
    caminho = f'./dados/calibracao/{metal.lower()}.csv'
    concentracoes = []
    correntes = []
    try:
        with open(caminho, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                concentracoes.append(float(row['concentracao_ugL']))
                correntes.append(float(row['corrente_uA']))
        return concentracoes, correntes
    except Exception as e:
        print(f"Erro ao carregar curva de calibração para {metal}: {e}")
        return None, None

def estimar_concentracao(curva_concentracoes, curva_correntes, corrente_pico):
    if not curva_concentracoes or not curva_correntes:
        return None
    a, b = np.polyfit(curva_concentracoes, curva_correntes, 1)
    if a == 0:
        return None
    concentracao = (corrente_pico - b) / a
    return concentracao