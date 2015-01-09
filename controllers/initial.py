# coding=UTF-8
import datetime, os, commands

def principal():
    response.title="Global"
    #if session.aut == '0':
    #    funcao = request.vars['f']
    #    redirect(URL("redireciona", "/%s" %(funcao)))
    tipo='global'
    con=db(Agenda.particular==False).select()

    return response.render("initial/principal.html", con=con, tipo=tipo)

def particular():
    response.title="Particular"
    if session.ramal == '0':
        redirect(URL("initial", "/log_in"))

    tipo='part'
    query=(Agenda.particular==True) & (Agenda.ramal == session.ramal)
    con=db(query).select()

    return response.render("initial/principal.html", con=con, tipo=tipo)

def ligacao():
    if session.ramal == '0':
        redirect(URL("initial", "/principal"))

    telefone = request.vars['n']
    ramal = str(session.ramal)
    #ramal_fis = str(session.ramal_fis)
    #tecnologia = str(session.tecnologia)
    funcao = request.vars['f']

    f = open('/tmp/000.cal','w')
    f.write('Channel: local/%s@permissao_ramaldestino\n' %(ramal))
    f.write('Context: ramais\n')
    f.write('Extension: %s\n' %(telefone))
    f.write('Callerid: agenda\nMaxRetries: 1\nRetryTime: 30\nWaitTime: 60')
    f.close()
    commands.getoutput("chmod 777 /tmp/000.cal")
    commands.getoutput("cp /tmp/000.cal /var/spool/asterisk/outgoing/")

    print 'Ligação do ramal %s para número %s' %(str(session.ramal), telefone)
    if request.vars['f'] == 'part':
        funcao = 'particular'
    else:
        funcao = 'principal'

    session.flash = "Ligação do ramal %s para número %s" %(str(session.ramal), telefone)
    redirect(URL("initial", "/%s" %(funcao)))

def adicionar():
    if session.ramal == '0':
        redirect(URL("initial", "/log_in"))

    response.title="Adicionar"
    id_edit = request.vars.id_edit

    if id_edit is None:
        if session.cadastro_agenda is False:
            db.f_agenda.particular.default = True
            db.f_agenda.particular.writable = False
        form = SQLFORM(db.f_agenda)
    else:
        print check_id_edit(id_edit)
        if session.cadastro_agenda is False:
            db.f_agenda.particular.default = True
            db.f_agenda.particular.writable = False
            if check_id_edit(id_edit) is False:
                redirect(URL("initial", "/principal"))

        form = SQLFORM(db.f_agenda, id_edit)
    
    form.custom.widget.ramal['_value'] = session.ramal
    if form.process().accepted:
        session.flash = 'Dados processados'
        if form.vars.particular is False:
            redirect(URL("initial", "/principal"))
        else:
            redirect(URL("initial", "/particular"))
    elif form.errors:
    	response.flash = 'Ops, algo não está correto'
    else:
    	response.flash = 'Insira os dados do formulário'
    return response.render("initial/adicionar.html", form=form)

def check_id_edit(id_edit):
    #checa se registro é particular
    print id_edit
    query = (Agenda.id == id_edit) & (Agenda.particular == True)
    if db(query).isempty():
        return False
    else:
        return True

def delete():
    print request.vars
    funcao  =   request.vars['tabela']
    id_tab  =   request.vars['id_tab']

    if (session.cadastro_agenda is False) & (check_id_edit(id_tab) is False):
        redirect(URL("initial", "/principal"))

    if funcao   == "global":
        funcao  =    'principal'  
        tabela  =    db.f_agenda.id
    if funcao   == "part":
        funcao  =    'particular'  
        tabela  =    db.f_agenda.id

    db(tabela == id_tab).delete()
    redirect(URL(funcao))


def log_in():
	#adicionar
    form = SQLFORM.factory(
    		Field("ramal", requires = IS_NOT_EMPTY(error_message=
						T("valor não pode ser nulo"))),
    		Field("senha", "password"),
    		formstyle="divs",
    		)

    response.title="Login"
    if form.process().accepted:
    	ramal_dig = form.vars.ramal
    	senha_dig = form.vars.senha
    	print 'ramal digitado:%s  senha digitada:%s' %(ramal_dig, senha_dig) 
        query = (Ramal_virtual.ramal_virtual == ramal_dig)&\
                (Ramal_virtual.id == Aplicacao.id_ramalvirtual)
        con = db(query).select(Ramal_virtual.nome, Ramal_virtual.ramal_virtual,
                             Aplicacao.agenda_senha, Aplicacao.agenda_cadastro)
        
        if db(query).isempty():
    		print "ramal incorreto"
    		response.flash = 'Ramal incorreto'
        else:
            usuario=con[0].f_ramal_virtual.nome
            senha=con[0].f_aplicacao.agenda_senha

            print 'usuario senha'
            print session.ramal, senha
            
            if senha_dig == str(senha):
                print "senha ok"
                session.ramal=con[0].f_ramal_virtual.ramal_virtual
                session.cadastro_agenda=con[0].f_aplicacao.agenda_cadastro
                #sem uso
                #session.ramal_fis=con[0].fisico_sip_iax.usuario
                #session.tecnologia=con[0].fisico_sip_iax.tecnologia

                print'login efetuado %s (log_in)' %(session.ramal)
                session.flash = 'Bem Vindo %s' %(usuario)
                redirect(URL("initial", "/principal"))
            else:
                print 'senha incorreta'
                response.flash = 'Senha incorreta'	
    return response.render("initial/show_form.html", form=form)


def log_out():
    session.aut='0'
    session.ramal='0'
    #session.ramal_fis='0'
    #session.tecnologia='0'
    session.cadastro_agenda = False
    print session.cadastro_agenda
    print "logout (log_out)"
    redirect(URL("initial", "/log_in"))

def teste1():
    print session
    ramal_dig = 8082
    query = (Ramal_virtual.ramal_virtual == ramal_dig)&\
                (Ramal_virtual.ramal_fisico == Fisico.usuario)&\
                (Ramal_virtual.id == Aplicacao.id_ramalvirtual)
    con = db(query).select(Ramal_virtual.nome, Ramal_virtual.ramal_virtual, Fisico.usuario, Fisico.secret, 
                    Fisico.tecnologia, Aplicacao.agenda_senha, Aplicacao.agenda_cadastro)
    #print con[0].fisico_sip_iax.secret
    tipo='global'
    perm='0'
    if ((tipo == 'global') and (perm != False)) or (tipo == 'part'):
        print 'mostra'

def redireciona():
    #sem uso
    if session.aut != '0':
        funcao = request.vars['f']
        redirect(URL("initial", "/%s" %(funcao)))
        #redirect(URL("initial", "/permissao?f=%s" %(funcao)))
    else:
        print 'ramal %s nao esta logado (redireciona)' %(session.aut)
        session.flash = "Faça o login"
        redirect(URL("initial", "/log_in"))