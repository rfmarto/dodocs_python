from flask import Flask, render_template, request, redirect, session, flash, url_for
from sistema import app, db
from models import Servico, Empresa, Evento, Finevento



def dtFormat(dt):
    if len(dt) > 10:
        fdt = dt.replace('T',' ')
        fdt = fdt +':00'
    else:
        fdt = dt[6:11]+'-'+dt[3:5]+'-'+dt[0:2]
    return fdt


@app.route('/')
def login():
    return render_template('/login/login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if( (request.form['user'] == 'roger' or request.form['user'] == 'dodocs' or request.form['user']== 'thatha') and
            (request.form['pass']== 'gato')):
        session['user'] = request.form['user']
        #flash(session['user'] + ' logado com sucesso')
        return redirect('/menu')
    else:
        flash('Usuário ou senha inválidos')
        return redirect('/')

@app.route('/logout')
def logout():
    session['user'] = None
    flash('Logout realizado com sucesso')
    return redirect('/')

@app.route('/menu')
def menu():
    if 'user' not in session or session['user'] == None:
        return redirect('/')
    return render_template('/menu/menu.html')

########################## EVENTO ##########################

@app.route('/list_evento')
def list_evento():
    sql = 'select  DATE_FORMAT(ev.dtIniRel, "%Y-%m-%d") dtIniRel, '
    sql = sql +'ev.cdOrganizadora, ev.nmEvento, ep.fantasia, ev.cdEvento '
    sql = sql +'from domanager.evento ev, domanager.empresa ep '
    sql = sql +'where ev.cdOrganizadora = ep.cdEmpresa order by dtIniRel'
    eventos = db.engine.execute(sql)
    return render_template('evento/evento.html', eventos=eventos)

@app.route('/add_evento')
def add_evento():

    return render_template('evento/add_evento.html')

@app.route('/valida_form',  methods=['POST'])
def valida_form():

    cnpjRel = request.form['cnpjRel']
    cnpjOrg = request.form['cnpjOrg']
    cnpjLoc = request.form['cnpjLoc']

    nmEvento = request.form['nmEvento']
    pax = request.form['pax']

    dtIniMont = request.form['dtIniMont']
    dtFimMont = request.form['dtFimMont']

    dtIniRel = request.form['dtIniRel']
    dtFimRel = request.form['dtFimRel']

    dtIniDesmont = request.form['dtIniDesmont']
    dtFimDesmont = request.form['dtFimDesmont']

    validado = 1

    rel = Empresa.query.filter_by(cnpj=cnpjRel).first()
    if not rel:
        flash('Empresa realizadora não cadastrada')

    org = Empresa.query.filter_by(cnpj=cnpjOrg).first()
    if not org:
        flash('Empresa organizadora não cadastrada')

    loc = Empresa.query.filter_by(cnpj=cnpjLoc).first()
    if not loc:
        flash('Empresa do local do evento não cadastrada')

    return render_template('/evento/add_evento.html', rel=rel, org=org, loc=loc, nmEvento=nmEvento, pax=pax, \
                           dtIniMont=dtIniMont, dtFimMont=dtFimMont, dtIniRel=dtIniRel,\
                           dtFimRel=dtFimRel, dtIniDesmont=dtIniDesmont, dtFimDesmont=dtFimDesmont, validado=validado)

@app.route('/addEvento', methods=['POST'])
def addEvento():

    nmEvento = request.form['nmEvento']
    pax = request.form['pax']


    dtIniMont = dtFormat(request.form['dtIniMont'])
    dtFimMont = dtFormat(request.form['dtFimMont'])

    dtIniRel = dtFormat(request.form['dtIniRel'])
    dtFimRel = dtFormat(request.form['dtFimRel'])

    dtIniDesmont = dtFormat(request.form['dtIniDesmont'])
    dtFimDesmont = dtFormat(request.form['dtFimDesmont'])

    cdRel = request.form['cdRel']
    cdOrg = request.form['cdOrg']
    cdLoc = request.form['cdLoc']

    existe = Evento.query.filter_by(cdRealizadora=cdRel,\
                                    cdOrganizadora=cdOrg,\
                                    cdLocal=cdLoc,
                                    dtIniRel=dtIniRel).first()
    if existe:
        flash('Evento já cadastrado')
        return redirect(url_for('valida_form'))



    new_evento = Evento(cdOrganizadora=cdOrg, cdRealizadora=cdRel, cdLocal=cdLoc, nmEvento=nmEvento, \
                          dtIniMont=dtIniMont, dtFimMont=dtFimMont, dtIniRel=dtIniRel, \
                          dtFimRel=dtFimRel, dtIniDesmont=dtIniDesmont, dtFimDesmont=dtFimDesmont, pax=pax)

    db.session.add(new_evento)
    db.session.commit()

    return render_template('evento/evento.html')

@app.route('/addProdutor')
def addProdutor():
    return render_template('evento/add_produtor.html')

@app.route('/contrato', methods=['POST',])
def contrato():
    return render_template('documentos/contrato.html')

########################## FINANCEIRO ##############################

@app.route('/financeiro/<int:cdEvento>')
def financeiro(cdEvento):

    fin = Finevento.query.filter_by(cdEvento=cdEvento).order_by(Finevento.dtLanc)

    sql = 'select sum(valor) as venda from domanager.finevento where cdevento = ' + str(cdEvento) + ' and valor > 0'
    venda = db.engine.execute(sql)
    for i in venda:
        vlVenda = i.venda

    sql = 'select sum(valor) as custo from domanager.finevento where cdevento = ' + str(cdEvento) + ' and valor < 0'
    custo = db.engine.execute(sql)
    for i in custo:
        vlCusto = i.custo

#################################################


#################################################
    sql = 'select ((sum(valor) / 100) * 6) as nf from domanager.finevento where cdevento = ' + str(cdEvento) + ' and valor > 0'
    nf = db.engine.execute(sql)
    for i in nf:
        vlNf = i.nf
        vlNf = (vlNf*-1)

    res = vlVenda - (vlCusto + vlNf)



    return render_template('/fin/finEve.html', fin=fin, venda=vlVenda, custo=vlCusto, nf=vlNf, res=res)


@app.route('/addLancamento', methods=['POST',])
def addLancamento():
    cdEvento = request.form['cdEvento']
    dt  =  request.form['data']
    det = request.form['detalhe']
    vl  = request.form['valor']

    newFinEvento = Finevento(cdEvento=cdEvento, detalhe=det, dtLanc=dt, valor=vl)
    db.session.add(newFinEvento)
    db.session.commit()

    fin = Finevento.query.filter_by(cdEvento=cdEvento).order_by(Finevento.dtLanc)

    sql = 'select sum(valor) venda from domanager.finevento where cdevento = '+str(cdEvento)+' and valor > 0'
    venda = db.engine.execute(sql)

    sql ='select sum(valor) custo from domanager.finevento where cdevento = '+str(cdEvento)+' and valor < 0'
    custo = db.engine.execute(sql)

    sql = 'select((sum(valor) / 100) * 6) nf from domanager.finevento where cdevento = '+str(cdEvento)+' and valor > 0'
    nf = db.engine.execute(sql)

    resultado = (venda.venda - custo.custo - nf.nf)


    return render_template('/fin/finEve.html', fin=fin, venda=venda, custo=custo, nf=nf, resultado=resultado)


########################## CLIENTE ##############################

@app.route('/cliente')
def cliente():
    return render_template('/cliente/cad_cliente.html')

@app.route('/add_cliente', methods=['POST',])
def add_cliente():
    req_cnpj = request.form['cnpj']
    req_razao = request.form['nome']
    req_fantasia = request.form['fantasia']
    req_email = request.form['email']
    req_fone = request.form['telefone']
    req_logradouro = request.form['logradouro']
    req_numero = request.form['numero']
    req_complemento = request.form['complemento']
    req_cep = request.form['cep']
    req_bairro = request.form['bairro']
    req_municipio = request.form['municipio']
    req_uf = request.form['uf']
    req_atividade = request.form['atividade_principal']
    req_cod_atividade = request.form['code']
    req_abertura = dtFormat(request.form['abertura'])




    existe = Empresa.query.filter_by(cnpj = req_cnpj).first()
    if existe:
        flash('Empresa já cadastrada')
        return redirect(url_for('list_cliente'))

    new_empresa = Empresa(cnpj=req_cnpj, razao=req_razao, fantasia=req_fantasia, email=req_email,\
                          fone=req_fone, logradouro=req_logradouro, numero=req_numero,\
                          complemento=req_complemento, cep=req_cep, bairro=req_bairro, uf=req_uf,\
                          atividade=req_atividade, cod_atividade=req_cod_atividade, abertura=req_abertura, municipio=req_municipio)

    db.session.add(new_empresa)
    db.session.commit()

    lista = Empresa.query.order_by(Empresa.razao)

    return render_template('/cliente/lista_cliente.html', empresas=lista)

@app.route('/list_cliente')
def list_cliente():
    emp = Empresa.query.order_by(Empresa.razao)
    return render_template('/cliente/lista_cliente.html', empresas=emp)

@app.route('/upd_cliente/<int:id>')
def upd_cliente(id):
    emp = Empresa.query.filter_by(cdEmpresa=id).first()

    return render_template('/cliente/upd_cliente.html', emp=emp)


########################## CONTATO ##############################

@app.route('/contato/cad_contato.html')
def cad_contato():
    return render_template('/contato/cad_contato.html')

@app.route('/contato/contato_by_cli/int:id')
def contato_by_cli(id):
    cont = Contato.query.filter_by(id=id).first()

    return render_template('/contato/contato.html')



##############################
@app.route('/evento/evento_by_cli/int:id', methods=['POST',])
def evento_by_cli(id):
    emp = Empresa.query.filter_by(id=id).first()

    return render_template('/evento/evento_by_cli.html')




@app.route('/servico')
def list_servico():
    lista = Servico.query.order_by(Servico.servico)
    return render_template('/servico/lista_servico.html', servicos=lista)

@app.route('/cad_servico')
def cad_servico():
    lista = Servico.query.order_by(Servico.servico)
    return render_template('/servico/cad_servico.html', servicos=lista)

@app.route('/add_servico', methods=['POST',])
def add_servico():
    servico = request.form['servico']

    existe = Servico.query.filter_by(servico=servico).first()
    if existe:
        flash('Serviço já existente')
        return redirect(url_for('list_servico'))

    new_servico = Servico(servico = servico)
    db.session.add(new_servico)
    db.session.commit()

    lista = Servico.query.order_by(Servico.servico)

    return render_template('/servico/cad_servico.html', servicos=lista)

