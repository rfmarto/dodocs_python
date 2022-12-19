from sistema import db


class Servico(db.Model):
    id_servico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    servico = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Profissao(db.Model):
    cdProfissao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profissao = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name



class Contato(db.Model):
    cdContato = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)
    fone = db.Column(db.String(45), nullable=False)
    celular = db.Column(db.String(450), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name



class Parceiro(db.Model):
    cdParceiro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    rg = db.Column(db.String(45), nullable=True)
    cpf = db.Column(db.String(450), nullable=True)
    crea = db.Column(db.String(450), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name

class Empresa(db.Model):
    cdEmpresa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpj = db.Column(db.String(200), nullable=False)
    razao: object = db.Column(db.String(200), nullable=False)
    fantasia = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    fone = db.Column(db.String(45), nullable=False)
    logradouro = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(45), nullable=True)
    complemento = db.Column(db.String(45), nullable=True)
    cep = db.Column(db.String(45), nullable=True)
    bairro = db.Column(db.String(200), nullable=True)
    municipio = db.Column(db.String(200), nullable=True)
    uf = db.Column(db.String(45), nullable=True)
    atividade = db.Column(db.String(500), nullable=True)
    cod_atividade = db.Column(db.String(45), nullable=True)
    abertura = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name

class Evento(db.Model):
    cdEvento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cdOrganizadora = db.Column(db.Integer, nullable=False)
    cdRealizadora = db.Column(db.Integer, nullable=False)
    cdLocal = db.Column(db.Integer, nullable=False)
    cdContato = db.Column(db.Integer, nullable=True)
    nmEvento = db.Column(db.String(200), nullable=False)
    dtIniMont = db.Column(db.DateTime, nullable=True)
    dtFimMont = db.Column(db.DateTime, nullable=True)
    dtIniRel = db.Column(db.DateTime, nullable=False)
    dtFimRel = db.Column(db.DateTime, nullable=True)
    dtIniDesmont = db.Column(db.DateTime, nullable=True)
    dtFimDesmont = db.Column(db.DateTime, nullable=True)
    pax = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name


class FinEvento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cdEvento = db.Column(db.Integer, nullable=False)
    detalhe = db.Column(db.String(200), nullable=False)
    dtLanc = db.Column(db.DateTime, nullable=False)
    valor = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name