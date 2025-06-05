let chat = document.querySelector('#chat');
let input = document.querySelector('#input');
let botaoEnviar = document.querySelector('#botao-enviar');
let imagemSelecionada;
let botaoAnexo = document.querySelector('#mais_arquivo');
let miniaturaImagem;


async function enviarMensagem() {
    if (input.value == "" && !imagemSelecionada) return;
    let mensagem = input.value;
    input.value = "";

    let novaBolha = criaBolhaUsuario();
    novaBolha.innerHTML = mensagem;

    if (imagemSelecionada) {
        let img = document.createElement('img');
        img.src = URL.createObjectURL(imagemSelecionada);
        img.style.maxWidth = "200px";
        img.style.display = "block";
        img.style.marginTop = "0.5rem";
        novaBolha.appendChild(img);

        if (miniaturaImagem) {
            miniaturaImagem.remove();
            miniaturaImagem = null;
        }
    }

    chat.appendChild(novaBolha);

    let novaBolhaBot = criaBolhaBot();
    chat.appendChild(novaBolhaBot);
    vaiParaFinalDoChat();
    novaBolhaBot.innerHTML = "Analisando...";

    // ENVIO PARA O BACKEND
    let resposta, dados;
    if (imagemSelecionada) {
        let formData = new FormData();
        formData.append('msg', mensagem);
        formData.append('imagem', imagemSelecionada);

        resposta = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            body: formData
        });
        dados = await resposta.json();
    } else {
        resposta = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({'msg':mensagem}),
        });
        dados = await resposta.json();
    }

    let html = dados.resposta.replace(/\n/g, '<br>');
    if (dados.imagem) {
        html += `<br><img src="${dados.imagem}" style="max-width: 300px; margin-top: 1rem;">`;
    }
    novaBolhaBot.innerHTML = html;
    vaiParaFinalDoChat();

    imagemSelecionada = null;
}

function criaBolhaUsuario() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    return bolha;
}

function criaBolhaBot() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    return bolha;
}

function vaiParaFinalDoChat() {
    chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener('click', enviarMensagem);
input.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        botaoEnviar.click();
    }
});

function limparConversa(){
    const limpar = fetch("http://127.0.0.1:5000/limpar_historico", {
        method: "POST"
    });
    chat.innerHTML = "<p class='chat__bolha chat__bolha--bot'>Olá! Eu sou o assistente virtual EnviroAI ~<br/><br/>Como posso te ajudar?</p>";
}

async function pegarImagem() {
    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';

    fileInput.onchange = e => {
        if (miniaturaImagem) {
            miniaturaImagem.remove(); 
        }

        imagemSelecionada = e.target.files[0];

        miniaturaImagem = document.createElement('img');
        miniaturaImagem.src = URL.createObjectURL(imagemSelecionada);
        miniaturaImagem.style.maxWidth = '3rem'; 
        miniaturaImagem.style.maxHeight = '3rem';
        miniaturaImagem.style.margin = '0.5rem'; 

        document.querySelector('.entrada__container').insertBefore(miniaturaImagem, input);
    }
    fileInput.click();
}

botaoAnexo.addEventListener('click', pegarImagem);