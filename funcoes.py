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
