from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('caos.html')

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

@app.route('/verlivro', methods=['POST'])
def verlivro():
    nome = request.form['nome']
    autor = request.form['autor']
    valor = int(request.form['valor'])
    if valor <= 30:
        mensagem = 'Esse livro está apto para as vendas!'
    else:
        mensagem = 'Esse livro não está apto para as vendas!'
    return render_template('livro_cadastrado.html', mensagem = mensagem, autor = autor, nome = nome)

if __name__ == "__main__":
    app.run()