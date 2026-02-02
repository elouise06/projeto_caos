from flask import Flask, render_template, request


livros = []

import json
from flask import flash, redirect
from utils import db, lm
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_mydb}"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/comunidade')
def comunidade():
    return render_template('comunidade.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/mercado')
def mercado():
    return render_template('mercado.html')

@app.route('/doacao')
def doacao():
    return render_template('doacao.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastrarlivro')
def cadastrarlivro():
    return render_template('cadastrar_livro.html')

@app.route('/verlivro', methods=['POST'])
def verlivro():
    nome = request.form['nome']
    autor = request.form['autor']
    valor = float(request.form['valor'])
    if valor <= 30:
        mensagem = 'Esse livro está apto para as vendas!'
    else:
        mensagem = 'Esse livro não está apto para as vendas!'

    livro = {
        'nome': nome,
        'autor': autor,
        'valor': valor,
        'mensagem': mensagem
    }
    livros.append(livro)
    return render_template('livro_cadastrado.html',livro = livro)

@app.route('/listalivros')
def listalivros():
    return render_template('lista_livro.html', livros=livros)

if __name__ == "__main__":
    app.run()
