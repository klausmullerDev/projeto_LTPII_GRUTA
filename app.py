from flask import Flask, render_template, request, redirect, url_for, flash
from funcoes import db, authenticate_user, add_trabalhador, obter_funcionarios_do_banco_de_dados

app = Flask(__name__)
app.secret_key = "chave_secreta"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = authenticate_user(user_name, password)

        if user:
            return render_template('dashboard.html', user=user)
        else:
            flash('Usuário ou senha incorretos', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('dashboard.html')

@app.route('/listar_funcionarios')
def listar_funcionarios():
    funcionarios = obter_funcionarios_do_banco_de_dados()
    return render_template('listar_funcionarios.html', funcionarios=funcionarios)

@app.route('/add_trabalhador', methods=['GET', 'POST'])
def add_trabalhador_route():
    if request.method == 'POST':
        nome = request.form['nome']
        cargo = request.form['cargo']
        data_contratacao = request.form['data_contratacao']
        salario = request.form['salario']
        telefone = request.form['telefone']
        email = request.form['email']

        add_trabalhador(db, nome, cargo, data_contratacao, salario, telefone, email)

        flash('Trabalhador inserido com sucesso!', 'success')
        return redirect(url_for('add_trabalhador_route'))

    return render_template('add_trabalhador.html')

if __name__ == '__main__':
    app.run(debug=True)
