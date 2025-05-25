from flask import Flask, render_template, request, redirect, url_for, flash
from models.pessoa import Pessoa
from controllers.pessoa_controller import PessoaController
from database import db, init_app
import re
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.db'
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Gera uma chave segura

# Inicializa o banco de dados
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

def campos_validos(nome, sobrenome):
    # 🐛 BUG-007 Fix - Validação backend: somente letras e espaços
    padrao = re.compile(r'^[A-Za-zÀ-ÿ\s]+$')
    return padrao.match(nome) and padrao.match(sobrenome)

def limpar_e_validar_cpf(cpf):
    # 🐛 BUG-008 Fix - Remove máscara e valida CPF com 11 dígitos numéricos
    cpf_numeros = re.sub(r'\D', '', cpf)
    if len(cpf_numeros) != 11 or not cpf_numeros.isdigit():
        return None
    
    # 🐛 BUG-009 Fix - Validação de dígitos verificadores
    def calcular_digito(cpf_parcial, fator):
        soma = sum(int(digito) * peso for digito, peso in zip(cpf_parcial, range(fator, 1, -1)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    primeiro_digito = calcular_digito(cpf_numeros[:9], 10)
    segundo_digito = calcular_digito(cpf_numeros[:10], 11)

    if cpf_numeros[-2:] != primeiro_digito + segundo_digito:
        return None

    return cpf_numeros

def data_nascimento_valida(data_str):
    # 🐛 BUG-010 Fix - Validação de data
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        return data <= datetime.today().date()
    except:
        return False


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_pessoa():
    if request.method == 'POST':
        try:
            cpf = request.form['cpf']
            # 🐛 BUG-006 Fix - Validação simples: evitar duplicidade de CPF
            if Pessoa.query.filter_by(cpf=cpf).first():
                flash('CPF já cadastrado!', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('cadastrar.html', dados=request.form)
            
            # 🐛 BUG-007 Fix - Validação backend: somente letras e espaços
            if not campos_validos(request.form['nome'], request.form['sobrenome']):
                flash('Nome e sobrenome devem conter apenas letras.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('cadastrar.html', dados=request.form)
            
            # 🐛 BUG-008 Fix - Remove máscara e valida CPF com 11 dígitos numéricos
            cpf = limpar_e_validar_cpf(request.form['cpf'])
            if not cpf:
                flash('CPF inválido. Digite exatamente 11 números.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('cadastrar.html', dados=request.form)
            
            # 🐛 BUG-010 Fix - Validação de data
            if not data_nascimento_valida(request.form['data_nascimento']):
                flash('Data de nascimento inválida. Não pode ser futura.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('cadastrar.html', dados=request.form)
            
            # 🐛 BUG-011 Fix - Validação de length
            if len(request.form['nome']) > 100 or len(request.form['sobrenome']) > 100:
                flash('Nome e sobrenome devem ter no máximo 100 caracteres.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('cadastrar.html', dados=request.form)

            PessoaController.salvar_pessoa(
                request.form['nome'],
                request.form['sobrenome'],
                cpf,
                request.form['data_nascimento']
            )
            flash('Pessoa cadastrada com sucesso!', 'success')
            return redirect(url_for('listar_pessoas'))
        except Exception as e:
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
            # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
            return render_template('cadastrar.html', dados=request.form)

    return render_template('cadastrar.html', dados=None)

@app.route('/listar')
def listar_pessoas():
    pessoas = Pessoa.query.all()
    return render_template('listar.html', pessoas=pessoas)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    if request.method == 'POST':
        try:
            novo_cpf = request.form['cpf']

            # 🐛 BUG-006 Fix - Evitar duplicidade de CPF ao editar outra pessoa
            cpf_existente = Pessoa.query.filter_by(cpf=novo_cpf).first()
            if cpf_existente and cpf_existente.id != id:
                flash('CPF já cadastrado em outro registro!', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('editar.html', pessoa=pessoa, dados=request.form)
            
            # 🐛 BUG-007 Fix - Validação backend: somente letras e espaços
            if not campos_validos(request.form['nome'], request.form['sobrenome']):
                flash('Nome e sobrenome devem conter apenas letras.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('editar.html', pessoa=pessoa, dados=request.form)
            
            # 🐛 BUG-008 Fix - Remove máscara e valida CPF com 11 dígitos numéricos
            novo_cpf = limpar_e_validar_cpf(request.form['cpf'])
            if not novo_cpf:
                flash('CPF inválido. Digite exatamente 11 números.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('editar.html', pessoa=pessoa, dados=request.form)
            
            # 🐛 BUG-010 Fix - Validação de data
            if not data_nascimento_valida(request.form['data_nascimento']):
                flash('Data de nascimento inválida. Não pode ser futura.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('editar.html', pessoa=pessoa, dados=request.form)
            
            # 🐛 BUG-011 Fix - Validação de length
            if len(request.form['nome']) > 100 or len(request.form['sobrenome']) > 100:
                flash('Nome e sobrenome devem ter no máximo 100 caracteres.', 'warning')
                # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
                return render_template('editar.html', pessoa=pessoa, dados=request.form)

            pessoa.nome = request.form['nome']
            pessoa.sobrenome = request.form['sobrenome']
            pessoa.cpf = novo_cpf
            pessoa.data_de_nascimento = request.form['data_nascimento']
            db.session.commit()
            flash('Pessoa atualizada com sucesso!', 'success')
            return redirect(url_for('listar_pessoas'))
        except Exception as e:
            flash(f'Erro ao atualizar: {str(e)}', 'danger')
            # 🐛 BUG-014 Fix - Manter dados já preenchidos ao receber erro
            return render_template('editar.html', pessoa=pessoa, dados=request.form)

    return render_template('editar.html', pessoa=pessoa, dados=None)

@app.route('/remover/<int:id>')
def remover_pessoa(id):
    try:
        pessoa = Pessoa.query.get_or_404(id)
        db.session.delete(pessoa)
        db.session.commit()
        flash('Pessoa removida com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao remover: {str(e)}', 'danger')
    return redirect(url_for('listar_pessoas'))

if __name__ == '__main__':
    app.run(debug=True)