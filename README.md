# CRUD de Registro de Pessoas

Sistema CRUD de gerenciamento de pessoas com validações e interface web. Permite cadastrar, editar, listar e remover registros. Desenvolvido com foco na realização de testes em qualidade de software.

---

## 🗂️ Estrutura do Projeto

```
crud-pessoas/
├── src/
│   ├── app.py                  # Arquivo principal da aplicação Flask
│   ├── database.py             # Configuração do banco SQLite com SQLAlchemy
│   ├── models/
│   │   └── pessoa.py           # Modelo de dados Pessoa
│   ├── controllers/
│   │   └── pessoa_controller.py # Lógica de controle CRUD
│   ├── templates/
│   │   ├── index.html          # Página inicial
│   │   ├── listar.html         # Listagem de pessoas
│   │   ├── cadastrar.html      # Formulário de cadastro
│   │   └── editar.html         # Formulário de edição
│   ├── static/
│   │   └── style.css           # Estilo da aplicação
│   ├── instance/
│       └── pessoas.db          # Banco de dados SQLite (gerado ao iniciar a aplicação)
├── features/
│   ├── pessoa.feature          # Testes BDD no formato Gherkin
│   ├── environment.py
│   └── steps/
│       └── pessoa_steps.py     # Implementação dos steps do Behave
├── venv/                       # Inicie o venv na raiz do projeto
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🧰 Tecnologias utilizadas

- **Python 3.10+**
- **SQLite + SQLAlchemy** — Banco de dados relacional e ORM
- **HTML/CSS** — Interface básica do usuário
- **Behave** — Testes comportamentais BDD com Gherkin
- **Git e Github**

---

## 🚀 Instalando CRUD de Pessoas

Para instalar o CRUD de Pessoas, siga estas etapas:

### Linux e macOS:
```bash
git clone https://github.com/seu-usuario/crud-pessoas.git
cd crud-pessoas
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows:
```bash
git clone https://github.com/mgpas/crud-pessoas.git
cd crud-pessoas
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ☕ Usando CRUD de Pessoas

Para usar o projeto localmente:

```bash
# Ative o ambiente virtual
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Inicie o servidor
python src/app.py
```

---

## 🧪 Testando CRUD de Pessoas

Para usar o projeto localmente:

```bash
# Execute o Behave (não execute o app.py ao mesmo tempo)
$env:PYTHONPATH="src"; behave features/
```

---

## 📋 Funcionalidades

- Cadastrar nova pessoa com validações de nome, sobrenome, CPF e data.
- Validar CPF duplicado, formato e dígitos verificadores.
- Validar nomes (letras apenas) e data de nascimento (sem datas futuras).
- Listar todas as pessoas cadastradas.
- Editar pessoa, mantendo regras de validação.
- Remover pessoa.
- Impedir envio de formulários com campos vazios.
- Garantir navegação correta (Página Inicial, Cancelar, Cadastrar Nova).

---

## ✅ Casos de Teste

| ID    | Nome do Caso de Teste                             | Tipo              | Pré-condições               | Passos                                                                 | Resultado Esperado                                                     |
|--------|---------------------------------------------------|-------------------|-----------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------|
| CT01 | Cadastro válido de pessoa                         | Funcional         | Sistema em execução         | Preencher nome, sobrenome, CPF e data válidos → Enviar                | Pessoa cadastrada e exibida na lista                                  |
| CT02 | Cadastro com CPF duplicado                        | Funcional         | Pessoa com CPF já existe    | Preencher CPF repetido → Enviar                                       | Alerta "CPF já cadastrado"                                            |
| CT03 | Cadastro com nome inválido                        | Funcional         | Sistema em execução         | Preencher nome como "João123" → Enviar                                | Alerta "Apenas letras"                                                |
| CT04 | Cadastro com data futura                          | Funcional         | Sistema em execução         | Preencher data como 2099-01-01 → Enviar                               | Alerta "Data de nascimento inválida"                                  |
| CT05 | Listagem de pessoas                               | Funcional         | Pessoa cadastrada           | Acessar rota `/listar`                                                | Ver os dados de todas as pessoas                                      |
| CT06 | Edição com dados válidos                          | Funcional         | Pessoa cadastrada           | Alterar dados corretamente → Enviar                                   | Dados atualizados                                                     |
| CT07 | Edição com CPF de outro registro                  | Funcional         | Duas pessoas cadastradas    | Editar uma usando CPF da outra → Enviar                               | Alerta "CPF já cadastrado"                                            |
| CT08 | Remoção de pessoa                                 | Funcional         | Pessoa cadastrada           | Clicar em "Remover"                                                   | Pessoa removida da lista                                              |
| CT09 | Cadastro com CPF inválido (<11 dígitos)           | Funcional         | Sistema em execução         | Informar CPF como "1234" → Enviar                                     | Alerta "CPF inválido"                                                 |
| CT10 | Cadastro com campos vazios                        | Funcional         | Sistema em execução         | Enviar sem preencher                                                  | Campos obrigatórios indicados                                        |
| CT11 | Validação de campos obrigatórios (required)       | Funcional / UI    | Sistema em execução         | Navegador impede envio com campos vazios                              | Sem submit, destaque nos campos                                       |
| CT13 | Link "Página Inicial" funciona                    | Navegação         | Acessar página de listagem  | Clicar em "Página Inicial"                                            | Redirecionado para `/`                                                |
| CT14 | Botão "Cancelar" na edição                        | Navegação         | Acessar tela de edição      | Clicar em "Cancelar"                                                  | Voltar para listagem                                                  |
| CT15 | "Cadastrar Nova Pessoa" leva ao formulário        | Navegação         | Acessar listagem            | Clicar no botão correspondente                                        | Redireciona para `/cadastrar`                                         |

## 📝 Licença

Esse projeto está sob licença MIT.
