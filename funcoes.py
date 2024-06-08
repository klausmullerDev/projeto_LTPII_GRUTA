import hashlib
from sql.banco import SQL

# Instanciando a classe SQL
db = SQL(servidor='localhost', usr='root', pwd='ceub123456', esquema='test')


def authenticate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    query = "SELECT * FROM tb_usr WHERE nme_usr=%s AND pwd_usr=%s"
    user = db.get_object(query, [username, hashed_password])
    return user


def add_trabalhador(db, nome, cargo, data_contratacao, salario, telefone, email):
    query = """
        INSERT INTO trabalhadores (nome, cargo, data_contratacao, salario, telefone, email) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    db.insert(query, [nome, cargo, data_contratacao, salario, telefone, email])


def obter_funcionarios_do_banco_de_dados():
    query = "SELECT * FROM trabalhadores"
    return db.get_list(query)


def obter_funcionarios_com_filtro(filtros):
    query = "SELECT * FROM trabalhadores WHERE 1=1"
    params = []

    if filtros['id']:
        query += " AND id = %s"
        params.append(filtros['id'])
    if filtros['nome']:
        query += " AND nome LIKE %s"
        params.append('%' + filtros['nome'] + '%')
    if filtros['cargo']:
        query += " AND cargo LIKE %s"
        params.append('%' + filtros['cargo'] + '%')
    if filtros['data_contratacao']:
        query += " AND data_contratacao = %s"
        params.append(filtros['data_contratacao'])
    if filtros['salario']:
        query += " AND salario = %s"
        params.append(filtros['salario'])
    if filtros['telefone']:
        query += " AND telefone LIKE %s"
        params.append('%' + filtros['telefone'] + '%')
    if filtros['email']:
        query += " AND email LIKE %s"
        params.append('%' + filtros['email'] + '%')

    return db.get_list(query, params)
