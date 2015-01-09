Agenda = db.define_table("f_agenda",
      Field("nome", notnull=True),
      Field("telefone", notnull=True),
      Field("obs"),
      Field("particular", "boolean"),
      Field("ramal", writable=True),
      #migrate=False,
      format="%(nome)s",
      migrate=False)

Ramal_virtual = db.define_table("f_ramal_virtual",
	Field("tecnologia", requires=IS_IN_SET(["SIP", "IAX2", "DAHDI", "KHOMP", "QUEUE", "FAX", "LOCAL", "MEETME"])),
	Field("ramal_fisico"),
	#Field("id_departamento", db.f_departamentos, requires=IS_IN_DB(db(db.f_departamentos.mostrar == True),'f_departamentos.id',"%(departamento)s")),
	Field("ramal_virtual"),
	Field("gravacao", "boolean"),
	Field("blacklist", "boolean"),
	Field("mesa_fop2", "boolean"),
	Field("chamadas_simultaneas", "integer"),
	#Field("id_grupo_destinos", db.f_grupo_destinos),
	Field("nome", "string", length="20"),
	Field("bina_interno"),
	Field("bina_externo"),
	Field("credito", "boolean"),
	format="%(ramal_virtual)s",
    migrate=False)

Fisico = db.define_table("fisico_sip_iax",
	Field("usuario"),
	Field("secret"),
	Field("tecnologia", requires=IS_IN_SET(["SIP", "IAX2"])),
	Field("type_f", requires=IS_IN_SET(["friend", "peer", "user"])),
	Field("host_f", "string", default="dynamic"),
	Field("context", "string", default="ramais"),
	Field("qualify", "boolean"),
	Field("disallow", "list:string"),
	Field("allow", "list:string"),
	Field("nat", "boolean"),
	Field("aut_externa", "boolean"),
	Field("tronco", "boolean", default=False),
	Field("extras", "text", default='requirecalltoken=no\ncanreinvite=no\n'),
	Field("register", "boolean"),
	format="%(usuario)s",
	migrate=False)

Aplicacao = db.define_table("f_aplicacao",
	Field("id_ramalvirtual", db.f_ramal_virtual),
	Field("cadeado_ativo", "boolean", default=False),
	Field("cadeado_senha"),
	Field("cs_ativo", "boolean", default=False),
	Field("cs_chamadaexterna", "boolean", default=False),
	Field("cs_chamadainterna", "boolean", default=False),
	Field("cs_numero", "integer"),
	Field("cs_excecao", "text"),
	Field("voicemail_ativo", "boolean", default=False),
	Field("voicemail_email"),
	Field("voicemail_senha", "integer"),
	Field("agenda_cadastro", "boolean", default=False),
	Field("agenda_senha", "integer"),
    migrate=False)

#agenda_lg = db.define_table("agenda_lg",
#      Field("ramal"),
#      Field("telefone"),
#      Field("empresa"),
#      Field("datetime"),
#      Field('particular'),
#      #auth.signature
#      format="%(nome)s")





