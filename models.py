from utils import db
from flask_login import UserMixin
from datetime import datetime, timezone

class Usuario(db.Model, UserMixin):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    nome_usuario = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(300), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    livros = db.relationship('Livro', backref='usuario', lazy=True)
    posts = db.relationship('Post', backref='usuario', lazy=True)
    comentarios = db.relationship('Comentario', backref='usuario', lazy=True)

    def __init__(self, nome, email, senha, nome_usuario, telefone):
        self.nome = nome
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha
        self.telefone = telefone
        
    
    def __repr__(self):
        return "<Usuario {}>".format(self.nome)

class Livro(db.Model):
    __tablename__= "livro"
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    ano_publicacao = db.Column(db.String(100), nullable=False)
    valor_desejado = db.Column(db.String(100))

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    def __init__(self, titulo, autor, genero, ano_publicacao, valor_desejado):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.ano_publicacao = ano_publicacao
        self.valor_desejado = valor_desejado
    
    def __repr__(self):
        return "<Livro {} - autor {}>".format(self.titulo, self.autor)
    
class Post(db.Model):
    __tablename__="post"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_postagem = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    comentarios = db.relationship('Comentario', backref='post', lazy=True)

    def __repr__(self):
        return "<Post {} do usuário {}>".format(self.id, self.usuario_id)
    
class Avaliacao(db.Model):
    __tablename__="avaliacao"
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=False)

    avaliador_id = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)
    avaliado_id = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)

    avaliador = db.relationship('Usuario',foreign_keys=[avaliador_id],backref='avaliacoes_feitas')
    avaliado = db.relationship('Usuario',foreign_keys=[avaliado_id],backref='avaliacoes_recebidas')

    def __init__(self, nota, comentario, avaliador_id, avaliado_id):
        if nota < 1 or nota > 5:
            raise ValueError("Nota inválida")
        self.nota = nota
        self.comentario = comentario
        self.avaliador_id = avaliador_id
        self.avaliado_id = avaliado_id

    def __repr__(self):
        return "<Avaliacao {}>".format(self.id)
    
class Comentario(db.Model):
    __tablename__="comentario"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_postagem = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return "<Comentario {}>".format(self.id)