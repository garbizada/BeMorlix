from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'bemorlix_secret_key'
DATABASE = 'usuarios.db'


# Função para conectar ao banco
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializa o banco com tabela de usuários
def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("Banco de dados inicializado.")

@app.context_processor
def inject_user():
    return dict(usuario_nome=session.get('usuario_nome'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        db = get_db()
        user = db.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['senha'], senha):
            session['usuario_id'] = user['id']
            session['usuario_nome'] = user['nome']
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos')

    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        senha_hash = generate_password_hash(senha)

        try:
            db = get_db()
            db.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                       (nome, email, senha_hash))
            db.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email já cadastrado.')
            return render_template('cadastro.html')
    else:
        return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/outlet')
def outlet():
    return render_template('outlet.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/escolha')
def escolha():
    return render_template('escolha.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

@app.route('/colecoes')
def colecoes():
    return render_template('colecoes.html')




# Servir arquivos estáticos se estiverem na mesma pasta
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
