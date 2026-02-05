from flask import Flask, render_template, request, flash, redirect, session
from utils import db, lm
import os
from flask_migrate import Migrate
from models import Usuario, Livro
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


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

@app.route('/')
def index():
    return render_template('caos.html')

@app.route('/cadastro/etapa1', methods=['GET', 'POST'])
def cadastro_etapa1():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        if not nome or not email or not telefone:
            flash("Preencha todos os campos", "warning")
            return redirect('/cadastro/etapa1')

        
        session['cadastro'] = {
            'nome': nome,
            'email': email,
            'telefone': telefone
        }

        return redirect('/cadastro/etapa2')

    return render_template('cadastro-dados.html')

@app.route('/cadastro/etapa2', methods=['GET', 'POST'])
def cadastro_etapa2():
    if 'cadastro' not in session:
        flash("Complete a primeira etapa do cadastro", "warning")
        return redirect('/cadastro/etapa1')
    
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario')
        senha = request.form.get('senha')

        if not nome_usuario or not senha:
            flash("Preencha todos os campos", "warning")
            return redirect('/cadastro/etapa2')

        
        dados = session['cadastro']
        nome = dados['nome']
        email = dados['email']
        telefone = dados['telefone']

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            telefone=telefone,
            nome_usuario=nome_usuario,
            senha=senha_hash
        )

        db.session.add(novo_usuario)
        db.session.commit()

        
        session.pop('cadastro')

       
        return redirect('/cadastro/sucesso')

    return render_template('cadastro-dados-2.html')

@app.route('/cadastro/sucesso')
def cadastro_sucesso():
    return render_template('cadastro-fim.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect('/inicio')
        else:
            flash('Dados incorretos')
            return redirect('/login')

    return render_template('login.html')

@lm.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/inicio')

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

@app.route('/perfil')
def perfil():
    return render_template('perfil_usuario.html')

if __name__ == "__main__":
    app.run()
