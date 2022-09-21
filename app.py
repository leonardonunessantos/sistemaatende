import datetime
from flask import Flask, render_template, redirect, request, url_for
from sqlalchemy import Integer, String, Date
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SECRET_KEY = 'nomeseguro'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)
logado = False


class Balanca(db.Model):
    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    datainsercao = db.Column('datainsercao', String(255), nullable=False)
    balanca = db.Column('balanca', String(255), nullable=False)
    nserie = db.Column('nserie', Integer)

    def __init__(self, datainsercao, balanca, nserie):
        self.datainsercao = datainsercao
        self.balanca = balanca
        self.nserie = nserie


class Peca(db.Model):
    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    datainsercao = db.Column('datainsercao', String(500), nullable=False)
    peca = db.Column('peca', String(255), nullable=False)
    nserie = db.Column('nserie', Integer)

    def __init__(self, datainsercao, peca, nserie):
        self.datainsercao = datainsercao
        self.peca = peca
        self.nserie = nserie


class Autorizada(db.Model):
    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    datainsercao = db.Column('datainsercao', String(500), nullable=False)
    autorizada = db.Column('autorizada', String(255), nullable=False)
    estado = db.Column('estado', String(255), nullable=False)
    cidade = db.Column('cidade', String(255), nullable=False)

    def __init__(self, datainsercao, autorizada, estado, cidade):
        self.datainsercao = datainsercao
        self.autorizada = autorizada
        self.estado = estado
        self.cidade = cidade


class Revenda(db.Model):
    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    datainsercao = db.Column('datainsercao', String(500), nullable=False)
    revenda = db.Column('revenda', String(255), nullable=False)
    estado = db.Column('estado', String(255), nullable=False)
    cidade = db.Column('cidade', String(255), nullable=False)

    def __init__(self, datainsercao, revenda, estado, cidade):
        self.datainsercao = datainsercao
        self.revenda = revenda
        self.estado = estado
        self.cidade = cidade


class Usuario(db.Model):
    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    datainsercao = db.Column('datainsercao', String(500), nullable=False)
    nomecompleto = db.Column('nome', String(255), nullable=False)
    email = db.Column('email', String(255), nullable=False)
    cargo = db.Column('cargo', String(255), nullable=False)
    senha = db.Column('senha', String(255), nullable=False)

    def __init__(self, datainsercao, nomecompleto, email, cargo, senha):
        self.datainsercao = datainsercao
        self.nomecompleto = nomecompleto
        self.email = email
        self.cargo = cargo
        self.senha = senha


class Ticket(db.Model):
    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    status = db.Column('status', String(60), nullable=False)
    revenda = db.Column('revenda', String(255), nullable=False)
    reclamacao = db.Column('reclamacao', String(500), nullable=False)
    dataabertura = db.Column('dataabertura', String(500), nullable=False)
    datafechamento = db.Column('datafechamento', String(60))
    modelo = db.Column('modelo', String(255), nullable=False)
    datacompra = db.Column('datacompra', Date, nullable=False)
    garantia = db.Column('garantia', String(60), nullable=False)
    resolucao = db.Column('resolucao', String(255), nullable=False)
    telefone = db.Column('telefone', String(60), nullable=False)
    estado = db.Column('estado', String(255), nullable=False)
    cidade = db.Column('cidade', String(255), nullable=False)
    autorizada = db.Column('autorizada', String(255), nullable=False)
    maodeobra = db.Column('maodeobra', Integer)
    notafiscal = db.Column('notafiscal', String(60))
    frete = db.Column('frete', Integer)
    envio = db.Column('envio', String(60))
    feedback = db.Column('feedback', String(100), nullable=False)
    usuario = db.Column('usuario', String(255), nullable=False)

    def __init__(self, status, revenda, reclamacao, dataabertura, datafechamento, modelo, datacompra, garantia, resolucao, telefone, estado, cidade, autorizada, maodeobra, notafiscal, frete, envio, feedback, usuario):
        self.status = status
        self.revenda = revenda
        self.reclamacao = reclamacao
        self.dataabertura = dataabertura
        self.datafechamento = datafechamento
        self.modelo = modelo
        self.datacompra = datacompra
        self.garantia = garantia
        self.resolucao = resolucao
        self.telefone = telefone
        self.estado = estado
        self.cidade = cidade
        self.autorizada = autorizada
        self.maodeobra = maodeobra
        self.notafiscal = notafiscal
        self.frete = frete
        self.envio = envio
        self.feedback = feedback
        self.usuario = usuario


def convertedata(data):
    print('Entrei na converte data')
    data_dia = int(data[8:])
    data_mes = int(data[5:7])
    data_ano = int(data[0:4])
    datacompleta = datetime.date(data_ano, data_mes, data_dia)
    print('Saindo da converte data')
    return datacompleta


def convertedata2(data):
    print('Entrei na converte data')
    data_dia = int(data[8:])
    data_mes = int(data[5:7])
    data_ano = int(data[0:4])
    datacompleta = str(data_dia) + '/' + str(data_mes) + '/' + str(data_ano)
    print('Saindo da converte data 2')
    return datacompleta


def esta_logado():
    print(logado)
    if logado:
        return True
    else:
        return False


@app.route('/')
def index():
    return render_template('login.html', falha_acesso=False)


@app.route('/autenticar', methods=['GET', 'POST'])
def autenticar():
    global logado
    usuarios = Usuario.query.all()
    lista_usuarios = []
    usuario_senha = {}
    for usuario in usuarios:
        lista_usuarios.append(usuario.email)
        usuario_senha[usuario.email] = usuario.senha
    if request.form['usuario'] in lista_usuarios:
        if request.form['senha'] == usuario_senha[request.form['usuario']]:
            logado = True
            return redirect(url_for('paineldecontrole'))
        else:
            print('Deu ruim... Senha incorreta')
            return render_template('login.html', falha_acesso='senha incorreta')
    else:
        print('Deu ruim...')
        return render_template('login.html', falha_acesso='usuario nao existe')


@app.route('/paineldecontrole', methods=['GET', 'POST'])
def paineldecontrole():
    if esta_logado():
        tickets = Ticket.query.all()
        n_ticket = 0
        for ticket in tickets:
            n_ticket += 1
        revendas = Revenda.query.all()
        n_revenda = 0
        for revenda in revendas:
            n_revenda += 1
        autorizadas = Autorizada.query.all()
        n_autorizada = 0
        for autorizada in autorizadas:
            n_autorizada += 1
        return render_template('paineldecontrole.html', tickets=tickets, n_ticket=n_ticket, n_revenda=n_revenda,    n_autorizada=n_autorizada)
    else:
        return redirect(url_for('index'))

# Tickets

@app.route('/gerenciamentotickets', methods=['GET', 'POST'])
def gerenciamentotickets():
    if esta_logado():
        tickets = Ticket.query.all()
        return render_template('gerenciamentotickets.html', tickets=tickets)
    else:
        return redirect(url_for('index'))


@app.route('/abrirticket', methods=['GET', 'POST'])
def abrirticket():
    if esta_logado():
        revendas = Revenda.query.all()
        autorizadas = Autorizada.query.all()
        balancas = Balanca.query.all()
        return render_template('abrirticket.html', revendas=revendas, autorizadas=autorizadas, balancas=balancas)
    else:
        return redirect(url_for('index'))


@app.route('/insereticket', methods=['POST', 'GET'])
def insereticket():
    if esta_logado():
        # Convertendo as datas para datas python
        print('Convertendo as datas')
        data = datetime.date.today()
        hoje = convertedata2(str(data))
        print('Pegando a data compra')
        print(request.form['datacompra'])
        datacompra = convertedata(request.form['datacompra'])
        # Inserindo as informações no banco
        print('1 - Inserindo informações no banco')
        ticket = Ticket('Em andamento', request.form['revenda'], request.form['reclamacao'], hoje, 'NULL', request.form ['modelo'], datacompra, request.form['garantia'], '', request.form['telefone'], request.form['uf'], request.form ['cidade'], request.form['autorizada'], '', '', '', '', '', 'Usuario')
        print('2 - Inserindo informações no banco')
        db.session.add(ticket)
        print('3 - Inserindo informações no banco')
        db.session.commit()
        print('4 - Inserindo informações no banco')
        return redirect('gerenciamentotickets')
    else:
        return redirect(url_for('index'))


@app.route('/editarticket/<int:id>', methods=['GET', 'POST'])
def editarticket(id):
    if esta_logado():
        ticket = Ticket.query.get(id)
        if request.method:
            if request.method == 'POST':
                ticket.revenda = request.form['revenda']
                ticket.reclamacao = request.form['reclamacao']
                ticket.modelo = request.form['modelo']
                ticket.datacompra = convertedata(request.form['datacompra'])
                ticket.telefone = request.form['telefone']
                ticket.estado = request.form['uf']
                ticket.cidade = request.form['cidade']
                ticket.autorizada = request.form['autorizada']
                db.session.commit()
                return redirect(url_for('gerenciamentotickets'))
            return render_template('editarticket.html', ticket=ticket)
        return render_template('gerenaciamentotickets.html', ticket=ticket)
    else:
        return redirect(url_for('index'))


@app.route('/verticket/<int:id>', methods=['GET', 'POST'])
def verticket(id):
    if esta_logado():
        ticket = Ticket.query.get(id)
        return render_template('verticket.html', ticket=ticket)
    else:
        return redirect(url_for('index'))


@app.route('/fecharticket/<int:id>', methods=['GET', 'POST'])
def fecharticket(id):
    if esta_logado():
        ticket = Ticket.query.get(id)
        if request.method:
            if request.method == 'POST':
                ticket.revenda = request.form['revenda']
                ticket.reclamacao = request.form['reclamacao']
                ticket.modelo = request.form['modelo']
                ticket.datacompra = convertedata(request.form['datacompra'])
                ticket.telefone = request.form['telefone']
                ticket.estado = request.form['uf']
                ticket.cidade = request.form['cidade']
                ticket.autorizada = request.form['autorizada']
                ticket.resolucao = request.form['resolucao']
                ticket.maodeobra = request.form['maodeobra']
                ticket.notafiscal = request.form['notafiscal']
                ticket.frete = request.form['frete']
                ticket.envio = request.form['envio']
                ticket.status = 'Finalizado'
                db.session.commit()
                tickets = Ticket.query.all()
                return render_template('gerenciamentotickets.html', tickets=tickets)
            return render_template('fecharticket.html', ticket=ticket)
        return render_template('gerenaciamentotickets.html', ticket=ticket)
    else:
        return redirect(url_for('index'))


@app.route('/excluirticket/<int:id>', methods=['GET'])
def excluirticket(id):
    if esta_logado():
        ticket = Ticket.query.get(id)
        db.session.delete(ticket)
        db.session.commit()
        return redirect(url_for('gerenciamentotickets'))
    else:
        return redirect(url_for('index'))


# Balança

@app.route('/gerenciamentobalancas', methods=['GET', 'POST'])
def gerenciamentobalancas():
    if esta_logado():
        balancas = Balanca.query.all()
        return render_template('gerenciamentobalancas.html', balancas=balancas)
    else:
        return redirect(url_for('index'))


@app.route('/cadastrarbalanca', methods=['GET', 'POST'])
def cadastrarbalanca():
    if esta_logado():
        return render_template('cadastrarbalanca.html')
    else:
        return redirect(url_for('index'))


@app.route('/inserebalanca', methods=['POST', 'GET'])
def inserebalanca():
    if esta_logado():
        # Convertendo as datas para datas python
        print('Convertendo as datas')
        data = datetime.date.today()
        hoje = convertedata2(str(data))
        # Inserindo as informações no banco
        print('1 - Inserindo informações no banco')
        print(request.form['nserie'])
        balanca = Balanca(hoje, request.form['balanca'], request.form['nserie'])
        print('2 - Inserindo informações no banco')
        db.session.add(balanca)
        print('3 - Inserindo informações no banco')
        db.session.commit()
        print('4 - Inserindo informações no banco')
        return redirect('gerenciamentobalancas')
    else:
        return redirect(url_for('index'))


@app.route('/editarbalanca/<int:id>', methods=['GET', 'POST'])
def editarbalanca(id):
    if esta_logado():
        balanca = Balanca.query.get(id)
        if request.method:
            if request.method == 'POST':
                balanca.balanca = request.form['balanca']
                balanca.nserie = request.form['nserie']
                db.session.commit()
                return redirect(url_for('gerenciamentobalancas'))
            return render_template('editarbalanca.html', balanca=balanca)
        return render_template('gerenaciamentobalancas.html', balanca=balanca)
    else:
        return redirect(url_for('index'))


@app.route('/excluirbalanca/<int:id>', methods=['GET'])
def excluirbalanca(id):
    if esta_logado():
        balanca = Balanca.query.get(id)
        db.session.delete(balanca)
        db.session.commit()
        return redirect(url_for('gerenciamentobalancas'))
    else:
        return redirect(url_for('index'))


# Peça

@app.route('/gerenciamentopecas', methods=['GET', 'POST'])
def gerenciamentopecas():
    if esta_logado():
        pecas = Peca.query.all()
        return render_template('gerenciamentopecas.html', pecas=pecas)
    else:
        return redirect(url_for('index'))


@app.route('/cadastrarpeca', methods=['GET', 'POST'])
def cadastrarpeca():
    if esta_logado():
        return render_template('cadastrarpeca.html')
    else:
        return redirect(url_for('index'))


@app.route('/inserepeca', methods=['POST', 'GET'])
def inserepeca():
    if esta_logado():
        # Convertendo as datas para datas python
        print('Convertendo as datas')
        data = datetime.date.today()
        hoje = convertedata2(str(data))
        # Inserindo as informações no banco
        print('1 - Inserindo informações no banco')
        peca = Peca(hoje, request.form['peca'], request.form['nserie'])
        print('2 - Inserindo informações no banco')
        db.session.add(peca)
        print('3 - Inserindo informações no banco')
        db.session.commit()
        print('4 - Inserindo informações no banco')
        return redirect('gerenciamentopecas')
    else:
        return redirect(url_for('index'))


@app.route('/editarpeca/<int:id>', methods=['GET', 'POST'])
def editarpeca(id):
    if esta_logado():
        peca = Peca.query.get(id)
        if request.method:
            if request.method == 'POST':
                peca.peca = request.form['peca']
                peca.nserie = request.form['nserie']
                db.session.commit()
                return redirect(url_for('gerenciamentopecas'))
            return render_template('editarpeca.html', peca=peca)
        return render_template('gerenaciamentopecas.html', peca=peca)
    else:
        return redirect(url_for('index'))


@app.route('/excluirpeca/<int:id>', methods=['GET'])
def excluirpeca(id):
    if esta_logado():
        peca = Peca.query.get(id)
        db.session.delete(peca)
        db.session.commit()
        return redirect(url_for('gerenciamentopecas'))
    else:
        return redirect(url_for('index'))


# Revendas

@app.route('/gerenciamentorevendas', methods=['GET', 'POST'])
def gerenciamentorevendas():
    if esta_logado():
        revendas = Revenda.query.all()
        return render_template('gerenciamentorevendas.html', revendas=revendas)
    else:
        return redirect(url_for('index'))


@app.route('/cadastrarrevenda', methods=['GET', 'POST'])
def cadastrarrevenda():
    if esta_logado():
        return render_template('cadastrarrevenda.html')
    else:
        return redirect(url_for('index'))


@app.route('/insererevenda', methods=['POST', 'GET'])
def insererevenda():
    if esta_logado():
        # Convertendo as datas para datas python
        print('Convertendo as datas')
        data = datetime.date.today()
        hoje = convertedata2(str(data))
        # Inserindo as informações no banco
        print('1 - Inserindo informações no banco')
        print(request.form['revenda'])
        revenda = Revenda(hoje, request.form['revenda'], request.form['estado'], request.form['cidade'])
        print('2 - Inserindo informações no banco')
        db.session.add(revenda)
        print('3 - Inserindo informações no banco')
        db.session.commit()
        print('4 - Inserindo informações no banco')
        return redirect('gerenciamentorevendas')
    else:
        return redirect(url_for('index'))


@app.route('/editarrevenda/<int:id>', methods=['GET', 'POST'])
def editarrevenda(id):
    if esta_logado():
        revenda = Revenda.query.get(id)
        if request.method:
            if request.method == 'POST':
                revenda.revenda = request.form['revenda']
                revenda.estado = request.form['estado']
                revenda.cidade = request.form['cidade']
                db.session.commit()
                return redirect(url_for('gerenciamentorevendas'))
            return render_template('editarrevenda.html', revenda=revenda)
        return render_template('gerenaciamentorevendas.html', revenda=revenda)
    else:
        return redirect(url_for('index'))


@app.route('/excluirrevenda/<int:id>', methods=['GET'])
def excluirrevenda(id):
    if esta_logado():
        revenda = Revenda.query.get(id)
        db.session.delete(revenda)
        db.session.commit()
        return redirect(url_for('gerenciamentorevendas'))
    else:
        return redirect(url_for('index'))


# Autorizadas

@app.route('/gerenciamentoautorizadas', methods=['GET', 'POST'])
def gerenciamentoautorizadas():
    if esta_logado():
        autorizadas = Autorizada.query.all()
        return render_template('gerenciamentoautorizadas.html', autorizadas=autorizadas)
    else:
        return redirect(url_for('index'))


@app.route('/cadastrarautorizada', methods=['GET', 'POST'])
def cadastrarautorizada():
    if esta_logado():
        return render_template('cadastrarautorizada.html')
    else:
        return redirect(url_for('index'))


@app.route('/insereautorizada', methods=['POST', 'GET'])
def insereautorizada():
    if esta_logado():
        # Convertendo as datas para datas python
        print('Convertendo as datas')
        data = datetime.date.today()
        hoje = convertedata2(str(data))
        # Inserindo as informações no banco
        print('1 - Inserindo informações no banco')
        autorizada = Autorizada(hoje, request.form['autorizada'], request.form['estado'], request.form['cidade'])
        print('2 - Inserindo informações no banco')
        db.session.add(autorizada)
        print('3 - Inserindo informações no banco')
        db.session.commit()
        print('4 - Inserindo informações no banco')
        return redirect('gerenciamentoautorizadas')
    else:
        return redirect(url_for('index'))


@app.route('/editarautorizada/<int:id>', methods=['GET', 'POST'])
def editarautorizada(id):
    if esta_logado():
        autorizada = Autorizada.query.get(id)
        if request.method:
            if request.method == 'POST':
                autorizada.autorizada = request.form['autorizada']
                autorizada.estado = request.form['estado']
                autorizada.cidade = request.form['cidade']
                db.session.commit()
                return redirect(url_for('gerenciamentoautorizadas'))
            return render_template('editarautorizada.html', autorizada=autorizada)
        return render_template('gerenaciamentoautorizadas.html', autorizada=autorizada)
    else:
        return redirect(url_for('index'))


@app.route('/excluirautorizada/<int:id>', methods=['GET'])
def excluirautorizada(id):
    if esta_logado():
        autorizada = Autorizada.query.get(id)
        db.session.delete(autorizada)
        db.session.commit()
        return redirect(url_for('gerenciamentoautorizadas'))
    else:
        return redirect(url_for('index'))


# Usuarios

@app.route('/gerenciamentousuarios', methods=['GET', 'POST'])
def gerenciamentousuarios():
    if esta_logado():
        usuarios = Usuario.query.all()
        return render_template('gerenciamentousuarios.html', usuarios=usuarios)
    else:
        return redirect(url_for('index'))


@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def cadastrarusuario():
    if esta_logado():
        return render_template('cadastrarusuario.html')
    else:
        return redirect(url_for('index'))


@app.route('/insereusuario', methods=['POST', 'GET'])
def insereusuario():
    if esta_logado():
        # Convertendo as datas para datas python
        print('Convertendo as datas')
        data = datetime.date.today()
        hoje = convertedata2(str(data))
        # Inserindo as informações no banco
        print('1 - Inserindo informações no banco')
        usuario = Usuario(hoje, request.form['nomecompleto'], request.form['email'], request.form['cargo'], request.form    ['senha'])
        print('2 - Inserindo informações no banco')
        db.session.add(usuario)
        print('3 - Inserindo informações no banco')
        db.session.commit()
        print('4 - Inserindo informações no banco')
        return redirect('gerenciamentousuarios')
    else:
        return redirect(url_for('index'))


@app.route('/editarusuario/<int:id>', methods=['GET', 'POST'])
def editarusuario(id):
    if esta_logado():
        usuario = Usuario.query.get(id)
        if request.method:
            if request.method == 'POST':
                usuario.nomecompleto = request.form['nomecompleto']
                usuario.email = request.form['email']
                usuario.cargo = request.form['cargo']
                usuario.senha = request.form['senha']
                db.session.commit()
                return redirect(url_for('gerenciamentousuarios'))
            return render_template('editarusuario.html', usuario=usuario)
        return render_template('gerenaciamentousuarios.html', usuario=usuario)
    else:
        return redirect(url_for('index'))


@app.route('/excluirusuario/<int:id>', methods=['GET'])
def excluirusuario(id):
    if esta_logado():
        usuario = Usuario.query.get(id)
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('gerenciamentousuarios'))
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # limpando a chave de usuario logado da session
    global logado
    logado = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)  # Sempre que salvar, o servidor vai dar um reload
