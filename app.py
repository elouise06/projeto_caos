from flask import Flask, render_template, request, flash, redirect, session, url_for
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for('index'))

@app.route('/livro/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_livro():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        ano_publicacao = request.form.get('ano_publicacao')
        tipo_capa = request.form.get('tipo_capa')
        troca = request.form.get('troca')
        genero = request.form.get('genero')
        valor_desejado = request.form.get('valor_desejado')

        if not titulo or not autor or not tipo_capa or not troca:
            flash("Preencha todos os campos obrigatórios", "warning")
            return redirect('/livro/cadastro')

        
        novo_livro = Livro(
            titulo=titulo,
            autor=autor,
            ano_publicacao=ano_publicacao,
            genero=genero,
            valor_desejado=valor_desejado,
            usuario_id=current_user.id
        )
        db.session.add(novo_livro)
        db.session.commit()

        
        return render_template('cadastro-livro-fim.html', livro=titulo)

    return render_template('cadastrar_livro.html')


@app.route('/livro/cadastro/fim', methods=['GET', 'POST'])
@login_required
def cadastro_livro_fim():
    return render_template('cadastro-livro-fim.html')

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
@login_required
def perfil():
    livros = current_user.livros
    return render_template('perfil_usuario.html', livros=livros, usuario=current_user)

@app.route('/usuario/atualizar', methods=['POST'])
@login_required
def atualizar_usuario():
    nome = request.form.get('nome')
    nome_usuario = request.form.get('nome_usuario')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    current_user.nome = nome
    current_user.nome_usuario = nome_usuario
    current_user.email = email
    current_user.telefone = telefone

    db.session.commit()
    flash("Dados atualizados com sucesso!", "success")
    return redirect(url_for('perfil'))

@app.route('/alterar_senha', methods=['POST'])
@login_required
def alterar_senha():
    senha_atual = request.form.get('senha_atual')
    nova_senha = request.form.get('nova_senha')

    if not check_password_hash(current_user.senha, senha_atual):
        flash("Senha atual incorreta!", "danger")
        return redirect(url_for('perfil'))

    if not nova_senha or len(nova_senha) < 6:
        flash("A nova senha deve ter pelo menos 6 caracteres.", "warning")
        return redirect(url_for('perfil'))

    current_user.senha = generate_password_hash(nova_senha)
    db.session.commit()
    flash("Senha atualizada com sucesso!", "success")
    return redirect(url_for('perfil'))

@app.route('/usuario/deletar', methods=['POST'])
@login_required
def deletar_usuario():
    user_id = current_user.id
    logout_user()
    usuario = Usuario.query.get_or_404(user_id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Sua conta foi deletada com sucesso.", "success")
    return redirect(url_for('index'))

@app.route('/livro/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)

    if livro.usuario_id != current_user.id:
        flash("Você não pode deletar este livro!", "danger")
        return redirect(url_for('perfil'))

    db.session.delete(livro)
    db.session.commit()
    flash("Livro deletado com sucesso!", "success")
    return redirect(url_for('perfil'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('acesso_negado_2.html'), 404

@app.errorhandler(401)
def unauthorized(error):
    return render_template('acesso_negado.html'), 401


if __name__ == "__main__":
    app.run()
