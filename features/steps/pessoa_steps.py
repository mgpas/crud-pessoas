from behave import given, when, then
from app import app
from database import db
from flask import g

app.testing = True

@given('que estou na página de cadastro')
def step_impl(context):
    context.client = app.test_client()
    context.form_data = {}

@when('eu preencho o nome "{nome}", sobrenome "{sobrenome}", CPF "{cpf}" e data de nascimento "{data_nascimento}"')
def step_impl(context, nome, sobrenome, cpf, data_nascimento):
    context.form_data = {
        "nome": nome,
        "sobrenome": sobrenome,
        "cpf": cpf,
        "data_nascimento": data_nascimento
    }

@when('clico em "Cadastrar"')
def step_impl(context):
    context.response = context.client.post("/cadastrar", data=context.form_data, follow_redirects=True)

@then('a nova pessoa deve aparecer na lista de pessoas')
def step_impl(context):
    response = context.client.get("/listar")
    assert context.form_data["nome"] in response.data.decode("utf-8")

@given('que já existe uma pessoa cadastrada com o CPF "52998224725"')
def step_impl(context):
    context.client = app.test_client()
    with app.app_context():
        from models.pessoa import Pessoa
        if not Pessoa.query.filter_by(cpf="52998224725").first():
            pessoa = Pessoa(nome="João", sobrenome="Silva", cpf="52998224725", data_de_nascimento="1990-05-10")
            db.session.add(pessoa)
            db.session.commit()

@when('eu tento cadastrar outra pessoa com o mesmo CPF')
def step_impl(context):
    context.response = context.client.post("/cadastrar", data={
        "nome": "Maria",
        "sobrenome": "Souza",
        "cpf": "52998224725",
        "data_nascimento": "1985-01-01"
    }, follow_redirects=True)

@then('devo ver a mensagem de erro "{mensagem}"')
def step_impl(context, mensagem):
    assert mensagem in context.response.data.decode("utf-8")

@when('eu tento cadastrar uma pessoa com o nome "{nome}"')
def step_impl(context, nome):
    context.response = context.client.post("/cadastrar", data={
        "nome": nome,
        "sobrenome": "Teste",
        "cpf": "16899535009",
        "data_nascimento": "1990-01-01"
    }, follow_redirects=True)

@when('eu tento cadastrar uma pessoa com a data de nascimento "{data_nascimento}"')
def step_impl(context, data_nascimento):
    context.response = context.client.post("/cadastrar", data={
        "nome": "Carlos",
        "sobrenome": "Teste",
        "cpf": "16899535009",
        "data_nascimento": data_nascimento
    }, follow_redirects=True)

@given('que existem pessoas cadastradas')
def step_impl(context):
    context.client = app.test_client()
    with app.app_context():
        from models.pessoa import Pessoa
        db.session.query(Pessoa).delete()
        pessoas = [
            Pessoa(nome="João", sobrenome="Silva", cpf="52998224725", data_de_nascimento="1990-05-10"),
            Pessoa(nome="Maria", sobrenome="Souza", cpf="16899535009", data_de_nascimento="1985-08-20"),
            Pessoa(nome="Lucas", sobrenome="Lima", cpf="04735895030", data_de_nascimento="1992-01-15")
        ]
        db.session.bulk_save_objects(pessoas)
        db.session.commit()

@when('eu acesso a página de listagem')
def step_impl(context):
    context.response = context.client.get("/listar")

@then('devo ver os dados de todas as pessoas cadastradas')
def step_impl(context):
    body = context.response.data.decode("utf-8")
    assert all(nome in body for nome in ["João", "Maria", "Lucas"])

@given('que uma pessoa está cadastrada')
def step_impl(context):
    context.client = app.test_client()
    with app.app_context():
        from models.pessoa import Pessoa
        pessoa = Pessoa(nome="Ana", sobrenome="Ferreira", cpf="11144477735", data_de_nascimento="1993-07-15")
        db.session.add(pessoa)
        db.session.commit()
        context.pessoa_id = pessoa.id

@when('eu acesso a tela de edição, altero os dados e clico em "Salvar"')
def step_impl(context):
    context.response = context.client.post(f"/editar/{context.pessoa_id}", data={
        "nome": "Ana Paula",
        "sobrenome": "Ferreira",
        "cpf": "11144477735",
        "data_nascimento": "1993-07-15"
    }, follow_redirects=True)

@then('os dados da pessoa devem ser atualizados corretamente')
def step_impl(context):
    assert "Ana Paula" in context.response.data.decode("utf-8")

@given('que existem duas pessoas cadastradas')
def step_impl(context):
    context.client = app.test_client()
    with app.app_context():
        from models.pessoa import Pessoa
        db.session.query(Pessoa).delete()
        p1 = Pessoa(nome="Pedro", sobrenome="Silva", cpf="86288381061", data_de_nascimento="1990-01-01")
        p2 = Pessoa(nome="Lucas", sobrenome="Almeida", cpf="28642762001", data_de_nascimento="1992-02-02")
        db.session.add_all([p1, p2])
        db.session.commit()
        context.id1 = p1.id
        context.id2 = p2.id

@when('eu tento editar uma usando o CPF da outra')
def step_impl(context):
    context.response = context.client.post(f"/editar/{context.id1}", data={
        "nome": "Pedro",
        "sobrenome": "Silva",
        "cpf": "28642762001",  # CPF duplicado
        "data_nascimento": "1990-01-01"
    }, follow_redirects=True)

@given('que existe uma pessoa cadastrada')
def step_impl(context):
    context.client = app.test_client()
    with app.app_context():
        from models.pessoa import Pessoa
        pessoa = Pessoa(nome="Lucas", sobrenome="Martins", cpf="75502825020", data_de_nascimento="1994-11-01")
        db.session.add(pessoa)
        db.session.commit()
        context.pessoa_id = pessoa.id

@when('eu clico em "Remover"')
def step_impl(context):
    context.response = context.client.get(f"/remover/{context.pessoa_id}", follow_redirects=True)

@then('a pessoa deve ser removida da lista')
def step_impl(context):
    with app.app_context():
        from models.pessoa import Pessoa
        pessoa = Pessoa.query.get(context.pessoa_id)
        assert pessoa is None
