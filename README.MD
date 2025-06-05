# 🌱 Enviro Mind

**Enviro Mind** é um sistema inteligente voltado à **análise e interpretação de dados eletroquímicos voltamétricos** (ex. ASV – Voltametria de Redissolução Anódica), com foco no **monitoramento ambiental de metais pesados em corpos hídricos**. O agente utiliza técnicas avançadas de **IA** para interpretar dados brutos e imagens de voltamogramas, estimar concentrações com base em curvas de calibração e verificar conformidade com padrões legais estabelecidos por **CONAMA, OMS e CETESB**.


https://drive.google.com/file/d/1PWwJRwmM8e7tKICu1S1JKCP9mZlMOOTX/view?usp=sharing

---

## Funcionalidades

- Assistente técnico com conhecimento especializado em voltametria, metais pesados e qualidade da água.
- Análise automatizada de dados (potencial vs. corrente) e imagens de voltamogramas.
- Estimativa precisa de concentrações via regressão linear com curvas de calibração específicas.
- Verificação automática de conformidade com limites legais (CONAMA 357/2005, OMS, CETESB).
- Geração de gráficos eletroquímicos diretamente a partir dos dados.
- Interface web intuitiva e responsiva com histórico de interação.
- Foco em respostas técnicas, claras e fundamentadas cientificamente.

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/daniirocca/EnviroMind.git
cd EnviroMind

# 2. Crie e ative o ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure sua chave da API da Anthropic
# Crie o arquivo .env com o seguinte conteúdo:
echo ANTHROPIC_API_KEY="sua-chave-aqui" > .env

# 5. Inicie a aplicação
python application.py
```

Acesse a aplicação em: [http://localhost:5000](http://localhost:5000)

---

## Estrutura do Projeto

```
EnviroMind/
├── application.py               # Inicialização da aplicação Flask
├── bot.py                       # Núcleo de interação com IA
├── analisador_de_imagens.py     # Análise de imagens de voltamogramas
├── helpers.py                   # Utilitários diversos
├── identificar_contexto.py      # Módulo contextual do chatbot
├── resumidor_de_historico.py    # Gerenciador de histórico
├── dados/
│   ├── calibracao/               # Arquivos de calibração por metal
│   │   ├── pb.csv
│   │   ├── cd.csv
│   │   ├── hg.csv
│   │   └── as.csv
│   ├── politicas_e_normativas.txt
│   └── dados_ambientais_eletroquimicos.txt
├── fotos/                       # Imagens processadas
├── historico/                   # Logs e interações
├── static/                      # Arquivos CSS, JS, imagens
├── templates/                   # Front-end HTML (Flask)
├── requirements.txt             # Dependências do projeto
└── .env                         # Variáveis de ambiente
```

---

## Como Utilizar

1. **Envie dados brutos** (potencial x corrente) ou uma **imagem de voltamograma** via chat.
2. O sistema irá:
   - Identificar os metais presentes.
   - Estimar a concentração com base em curvas de calibração.
   - Comparar com os limites legais vigentes.
   - Gerar gráficos automaticamente a partir dos dados.

---

## Licença

Distribuído sob os termos especificados no arquivo `LICENSE`.

---

**Enviro Mind** – Inteligência Artificial aplicada à vigilância ambiental, com base científica, foco regulatório e precisão eletroquímica.


Acesse também o Agente GPT inspirado na aplicação: https://chatgpt.com/g/g-6838d57619b88191a0c670f780ae3c0c-gpt-enviro
