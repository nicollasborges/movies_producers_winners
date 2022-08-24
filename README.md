# Filmes e produtores

Esta api inicia carregando uma lista de filmes em memoria, e já deixa calculado o intervalo minimo e maximo entre os ganhadores
Toda vez que é adicionado ou atualizado um filme novo, será recalculado o intervalo minimo e maximo

## 🚀 Começando

Clonar respositorio https://github.com/nicollasborges/movies_producers_winners.git

### 📋 Pré-requisitos
<p>python==3.9.0</p>
<p>fastapi==0.79.1</p>
<p>uvicorn==0.18.2</p>
<p>SQLAlchemy==1.4.40</p>
<p>pytest==7.1.2</p>
<p>requests==2.28.1</p>
<p>httpx==0.23.0</p>
<p>trio==0.21.0</p>

Rodar comando pip install -r requirements.txt


### 🔧 Instalação

<p>Rodar comando python main.py</p>

<p>acessar http://127.0.0.1:8000/docs</p>

![exemplo consultas](exemplo_consulta.png)


## ⚙️ Executando os testes

Testes inicia a criar o db em memória, após isso testa as rotas

Executar comando pytest

## 📦 Desenvolvimento

Adicione notas adicionais sobre como implantar isso em um sistema ativo

## 🛠️ Construído com

<p>FastAPI e SQLAlchemy, dois frameworks muito uteis</p> 
<p>FastApi para manipular de rotas</p>
<p>SQLAlchemy ORM para manipular db em memória</p>

## ✒️ Autores

* **Nicollas Neumann Borges** [desenvolvedor]https://github.com/nicollasborges)
