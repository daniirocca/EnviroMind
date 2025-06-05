from flask import Flask, render_template, request, Response, jsonify
from bot import bot 
import os
from helpers import *
from resumidor_de_historico import criar_resumo
import uuid
import shutil


application = Flask(__name__)
application.secret_key = "secret!@#"


PASTA_DE_UPLOAD = 'fotos'
caminho_da_imagem = None

@application.route("/")
def home():
    return render_template("index.html")

@application.route("/chat", methods=['POST'])
def chat():
    global caminho_da_imagem
    if request.content_type.startswith('multipart/form-data'):
        prompt = request.form.get('msg', '')
        imagem = request.files.get('imagem')
        if imagem:
            caminho_da_imagem = f'fotos/{imagem.filename}'
            imagem.save(caminho_da_imagem)
        else:
            caminho_da_imagem = None
    else:
        prompt = request.json['msg']
        caminho_da_imagem = None

    nome_do_arquivo = './historico/historico.txt'
    historico = ''
    if os.path.exists(nome_do_arquivo):
        historico = carrega(nome_do_arquivo)
    historico_resumido = criar_resumo(historico)
    resposta, caminho_da_imagem, caminho_imagem_estatica = bot(prompt, historico_resumido, caminho_da_imagem)
    conteudo = f"""
    Histórico: {historico_resumido}
    Usuário: {prompt}
    IA: {resposta}
    """
    salva(nome_do_arquivo, conteudo)
    return jsonify({'resposta': resposta, 'imagem': f'/{caminho_imagem_estatica}' if caminho_imagem_estatica else None})

@application.route("/limpar_historico", methods=["POST"])
def limpar_historico():
    caminho_historico = './historico/historico.txt'
    if os.path.exists(caminho_historico):
        os.remove(caminho_historico)
    pasta_fotos = 'fotos'
    if os.path.exists(pasta_fotos):
        for arquivo in os.listdir(pasta_fotos):
            caminho_arquivo = os.path.join(pasta_fotos, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
    return {}

@application.route("/upload_imagem", methods=['POST'])
def upload_imagem():
    global caminho_da_imagem
    if 'imagem' in request.files:
        imagem_enviada_no_chatbot = request.files['imagem']
        nome_do_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada_no_chatbot.filename)[1]
        caminho_do_arquivo = os.path.join(PASTA_DE_UPLOAD, nome_do_arquivo)
        imagem_enviada_no_chatbot.save(caminho_do_arquivo)
        caminho_da_imagem = caminho_do_arquivo
        return 'Imagem recebida com sucesso!', 200
    return 'Nenhum arquivo foi enviado', 400

if __name__ == "__main__":
    application.run(debug=True)
