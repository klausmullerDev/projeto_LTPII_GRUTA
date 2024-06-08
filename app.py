from flask import Flask, render_template, request, redirect, url_for, flash
from funcoes import db, authenticate_user, add_trabalhador, obter_funcionarios_do_banco_de_dados, \
    obter_funcionarios_com_filtro

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


@app.route('/listar_funcionarios', methods=['GET', 'POST'])
def listar_funcionarios():
    filtros = {
        'id': request.form.get('id'),
        'nome': request.form.get('nome'),
        'cargo': request.form.get('cargo'),
        'data_contratacao': request.form.get('data_contratacao'),
        'salario': request.form.get('salario'),
        'telefone': request.form.get('telefone'),
        'email': request.form.get('email')
    }
    funcionarios = obter_funcionarios_com_filtro(filtros)
    total_funcionarios = len(funcionarios)
    total_salarios = sum(func['salario'] for func in funcionarios)
    return render_template('listar_funcionarios.html', funcionarios=funcionarios, total_funcionarios=total_funcionarios,
                           total_salarios=total_salarios)


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


@app.route('/editar_trabalhador/<int:id>', methods=['GET', 'POST'])
def editar_trabalhador_route(id):
    if request.method == 'POST':
        nome = request.form['nome']
        cargo = request.form['cargo']
        data_contratacao = request.form['data_contratacao']
        salario = request.form['salario']
        telefone = request.form['telefone']
        email = request.form['email']

        query = """
            UPDATE trabalhadores 
            SET nome=%s, cargo=%s, data_contratacao=%s, salario=%s, telefone=%s, email=%s 
            WHERE id=%s
        """
        db.upd_del(query, [nome, cargo, data_contratacao, salario, telefone, email, id])

        flash('Trabalhador atualizado com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    trabalhador = db.get_object("SELECT * FROM trabalhadores WHERE id=%s", [id])
    return render_template('editar_trabalhador.html', trabalhador=trabalhador)


@app.route('/remover_trabalhador/<int:id>', methods=['GET', 'POST'])
def remover_trabalhador_route(id):
    if request.method == 'POST':
        query = "DELETE FROM trabalhadores WHERE id=%s"
        db.upd_del(query, [id])

        flash('Trabalhador removido com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    trabalhador = db.get_object("SELECT * FROM trabalhadores WHERE id=%s", [id])
    return render_template('remover_trabalhador.html', trabalhador=trabalhador)


if __name__ == '__main__':
    app.run(debug=True)
