# language: pt
Funcionalidade: Gerenciamento de Pessoas
  Como um usuário do sistema
  Eu quero cadastrar, listar, editar e remover pessoas
  Para manter um controle eficiente de registros

  Cenário: Cadastro de pessoa com dados válidos
    Dado que estou na página de cadastro
    Quando eu preencho o nome "João", sobrenome "Silva", CPF "12345678901" e data de nascimento "1990-05-10"
    E clico em "Cadastrar"
    Então a nova pessoa deve aparecer na lista de pessoas

  Cenário: Cadastro com CPF duplicado
    Dado que já existe uma pessoa cadastrada com o CPF "12345678901"
    Quando eu tento cadastrar outra pessoa com o mesmo CPF
    Então devo ver a mensagem de erro "CPF já cadastrado!"

  Cenário: Cadastro com nome inválido
    Quando eu tento cadastrar uma pessoa com o nome "João123"
    Então devo ver a mensagem de erro "Nome e sobrenome devem conter apenas letras."

  Cenário: Cadastro com data de nascimento futura
    Quando eu tento cadastrar uma pessoa com a data de nascimento "2099-01-01"
    Então devo ver a mensagem de erro "Data de nascimento inválida. Não pode ser futura."

  Cenário: Listagem de pessoas cadastradas
    Dado que existem pessoas cadastradas
    Quando eu acesso a página de listagem
    Então devo ver os dados de todas as pessoas cadastradas

  Cenário: Edição de pessoa com sucesso
    Dado que uma pessoa está cadastrada
    Quando eu acesso a tela de edição, altero os dados e clico em "Salvar"
    Então os dados da pessoa devem ser atualizados corretamente

  Cenário: Edição com CPF duplicado
    Dado que existem duas pessoas cadastradas
    Quando eu tento editar uma usando o CPF da outra
    Então devo ver a mensagem de erro "CPF já cadastrado!"

  Cenário: Remoção de pessoa cadastrada
    Dado que existe uma pessoa cadastrada
    Quando eu clico em "Remover"
    Então a pessoa deve ser removida da lista
