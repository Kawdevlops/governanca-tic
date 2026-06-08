// Criando as subprefeituras, responsáveis e equipes de tic

// SUB-AF - Aricanduva / Formosa / Carrão
MERGE (o:OrgaoSetorial {name: 'SUB-AF'})
SET o.sigla = 'SUB-AF',
    o.nome = 'Aricanduva / Formosa / Carrão',
    o.endereço = 'Rua Atucuri, 699',
    o.cep = '03411-000',
    o.telefone_fixo = '3396-0800',
    o.grupo_sdwan = 'subafsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'vbarcelos'})
SET r.nome = 'Valdir Benedito Rodrigues Barcelos',
    r.telefone_fixo = '3396-0821',
    r.telefone_movel = '99831-8686',
    r.email = 'vbarcelos@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'ljuvencio'})
SET e1.nome = 'Leandro Oliveira Juvencio',
    e1.telefone_movel = '97315-7370',
    e1.email = 'ljuvencio@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'alcidespsilva'})
SET e2.nome = 'Alcides Pereira da Silva',
    e2.telefone_fixo = '3396-0821',
    e2.email = 'alcidespsilva@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o)

MERGE (e3:Pessoa {name: 'nhiroshi'})
SET e3.nome = 'Nelson Hiroshi Oide',
    e3.telefone_movel = '97851-3358',
    e3.email = 'nhiroshi@smsub.prefeitura.sp.gov.br'
MERGE (e3)-[:EQUIPE_TIC_EM]->(o);

// SUB-BT - Butantã
MERGE (o:OrgaoSetorial {name: 'SUB-BT'})
SET o.sigla = 'SUB-BT',
    o.nome = 'Butantã',
    o.endereço = 'Rua Ulpiano da Costa Manso, 201',
    o.cep = '05538-000',
    o.telefone_fixo = '3397-4600',
    o.grupo_sdwan = 'subbtsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'vcosta'})
SET r.nome = 'Victor Davi Fernandes Martins Costa',
    r.telefone_fixo = '3397-4515',
    r.telefone_movel = '96837-4988',
    r.email = 'vcosta@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'apteles'})
SET e1.nome = 'Alessandra Paes Teles',
    e1.telefone_fixo = '3397-4515',
    e1.email = 'apteles@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-CL - Campo Limpo	
MERGE (o:OrgaoSetorial {name: 'SUB-CL'})
SET o.sigla = 'SUB-CL',
    o.nome = 'Campo Limpo',
    o.endereço = 'Rua Nossa Senhora do Bom Conselho, 59',
    o.cep = '05763-470',
    o.telefone_fixo = '3397-0500',
    o.grupo_sdwan = 'subclsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'darcioamerico'})
SET r.nome = 'Darcio Luiz Americo Silva',
    r.telefone_fixo = '3397-0564',
    r.telefone_movel = '[94598-6415, 94162-9240]',
    r.email = 'darcioamerico@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'acmendes'})
SET e1.nome = 'Andreia Cristina Souza Mendes',
    e1.telefone_fixo = '3397-0573',
    e1.email = 'acmendes@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB - CS - Capela do Socorro
MERGE (o:OrgaoSetorial {name: 'SUB-CS'})
SET o.sigla = 'SUB-CS',
    o.nome = 'Capela do Socorro',
    o.endereço = 'Rua Cassiano dos Santos, 499',
    o.cep = '04827-110',
    o.telefone_fixo = '3397-2700',
    o.grupo_sdwan = 'subcssdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'edmilsonmoraes'})
SET r.nome = 'Edmilson Atanásio de Moraes Junior',
    r.telefone_fixo = '3397-2716',
    r.telefone_movel = '98351-6716',
    r.email = 'edmilsonmoraes@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'luizjunior'})
SET e1.nome = 'Luiz Carlos Gonçalves Reis Jr',
    e1.email = 'luizjunior@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-CV - Casa Verde
MERGE (o:OrgaoSetorial {name: 'SUB-CV'})
SET o.sigla = 'SUB-CV',
    o.nome = 'Casa Verde',
    o.endereço = 'Av. Ordem e Progresso, 1001',
    o.cep = '02518-130',
    o.telefone_fixo = '3855-3800',
    o.grupo_sdwan = 'subcvsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'ljcruz'})
SET r.nome = 'Leandro José Santos da Cruz',
    r.telefone_fixo = '3855-3820',
    r.telefone_movel = '99354-3544',
    r.email = 'ljcruz@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'jrcoliveira'})
SET e1.nome = 'José Renato Coelho de Oliveira',
    e1.telefone_fixo = '3855-3803',
    e1.email = 'jrcoliveira@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'wjthomaz'})
SET e2.nome = 'William de Jesus Thomaz',
    e2.telefone_fixo = '3855-3820',
    e2.email = 'wjthomaz@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:ESTAGIARIO_TIC_EM]->(o)

MERGE (e3:Pessoa {name: 'ppacheco'})
SET e3.nome = 'Pedro Henrique Pacheco',
    e3.email = 'ppacheco@smsub.prefeitura.sp.gov.br'
MERGE (e3)-[:ESTAGIARIO_TIC_EM]->(o);

// SUB-AD - Cidade Ademar
MERGE (o:OrgaoSetorial {name: 'SUB-AD'})
SET o.sigla = 'SUB-AD',
    o.nome = 'Cidade Ademar',
    o.endereço = 'Av. Yervant Kissajikian, 416',
    o.cep = '04657-000',
    o.telefone_fixo = '5670-7000',
    o.grupo_sdwan = 'subadsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'acirandrade'})
SET r.nome = 'Acir Lopes de Andrade',
    r.telefone_fixo = '5670-7056',
    r.telefone_movel = '99558-9269',
    r.email = 'acirandrade@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'cleolima'})
SET e1.nome = 'Cleo Lima Junior',
    e1.telefone_fixo = '3201-2122',
    e1.email = 'cleolima@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'herbertsilva'})
SET e2.nome = 'Herbert Caetano da Silva',
    e2.telefone_fixo = '3201-2116',
    e2.email = 'herbertsilva@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o);

// SUB-CT - Cidade Tiradentes
MERGE (o:OrgaoSetorial {name: 'SUB-CT'})
SET o.sigla = 'SUB-CT',
    o.nome = 'Cidade Tiradentes',
    o.endereço = 'Rua Juá Mirim, 135',
    o.cep = '08490-800',
    o.telefone_fixo = '3396-0075',
    o.grupo_sdwan = 'subctsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'svilela'})
SET r.nome = 'Samuel Vilela',
    r.telefone_fixo = '3396-0075',
    r.ramal = '0071',
    r.telefone_movel = '96226-5551',
    r.email = 'svilela@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'celsospereira'})
SET e1.nome = 'Celso de Souza Pereira',
    e1.email = 'celsospereira@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-EM - Ermelindo Matarazzo
MERGE (o:OrgaoSetorial {name: 'SUB-EM'})
SET o.sigla = 'SUB-EM',
    o.nome = 'Ermelindo Matarazzo',
    o.endereço = 'Av. São Miguel, 5550',
    o.cep = '03871-100',
    o.telefone_fixo = '2114-0333',
    o.grupo_sdwan = 'subemsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'agasperini'})
SET r.nome = 'Alecio Gasperine Júnior',
    r.telefone_fixo = '2026-9326',
    r.telefone_movel = '97193-9941',
    r.email = 'agasperini@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'claudiosoares'})
SET e1.nome = 'Claudio Soares Ferreira',
    e1.telefone_fixo = '2026-9407',
    e1.telefone_movel = '99490-4368',
    e1.email = 'claudiosoares@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-FB
MERGE (o:OrgaoSetorial {name: 'SUB-FB'})
SET o.sigla = 'SUB-FB',
    o.nome = 'Freguesia / Brasilância',
    o.endereço = 'Av. João Marcelino Branco, 95',
    o.cep = '02610-000',
    o.telefone_fixo = '3981-5000',
    o.email = 'subgagti@smsub.prefeitura.sp.gov.br',
    o.grupo_sdwan = 'subfbsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'marcelobizerra'})
SET r.nome = 'Marcelo Bizerra',
    r.telefone_movel = '99396-6068',
    r.email = 'marcelobizerra@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'egrazina'})
SET e1.nome = 'Erick Henrique Grazina',
    e1.telefone_fixo = '3981-5058',
    e1.email = 'egrazina@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-G - Guaianases
MERGE (o:OrgaoSetorial {name: 'SUB-G'})
SET o.sigla = 'SUB-G',
    o.nome = 'Guaianases',
    o.endereço = 'Rua Hipólito de Camargo, 479',
    o.cep = '08410-030',
    o.telefone_fixo = '2392-1030',
    o.grupo_sdwan = ''

MERGE (r:Pessoa {name: 'gmartelo'})
SET r.nome = 'Gabriel Queiroz da Silva Martelo',
    r.telefone_fixo = '2392-1030',
    r.telefone_movel = '97735-0090',
    r.email = 'gmartelo@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'subgsdwan'})
SET e1.nome = 'Gustavo Henrique Ricardo',
    e1.telefone_fixo = '2392-1030',
    e1.email = 'subgsdwan@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'nazevedo'})
SET e2.nome = 'Nicolas Mariano de Azevedo',
    e2.telefone_fixo = '2392-1030'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o)

MERGE (e3:Pessoa {name: 'rmacedo'})
SET e3.nome = 'Rya Ferreira Macedo',
    e3.telefone_fixo = '2392-1030',
    e3.email = 'rmacedo@smsub.prefeitura.sp.gov.br'
MERGE (e3)-[:EQUIPE_TIC_EM]->(o)

MERGE (e4:Pessoa {name: 'oarf'})
SET e4.nome = 'Otávio Arf Júnior',
    e4.telefone_fixo = '2392-1030',
    e4.email = 'oarf@smsub.prefeitura.sp.gov.br'
MERGE (e4)-[:EQUIPE_TIC_EM]->(o);

// SUB-IP - Ipiranga
MERGE (o:OrgaoSetorial {name: 'SUB-IP'})
SET o.sigla = 'SUB-IP',
    o.nome = 'Ipiranga',
    o.endereço = 'Rua Lino Coutinho, 444',
    o.cep = '04207-000',
    o.telefone_fixo = '3540-0307',
    o.grupo_sdwan = 'subipsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'lfbarlotti'})
SET r.nome = 'Luis Felipe Pereira Barlotti',
    r.telefone_fixo = '3540-0350',
    r.telefone_movel = '99212-6666',
    r.email = 'lfbarlotti@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'mhsousa'})
SET e1.nome = 'Marcelo Henrique Anastacio de Sousa',
    e1.telefone_fixo = '3540-0351',
    e1.email = 'mhsousa@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-IT - Itaim Paulista
MERGE (o:OrgaoSetorial {name: 'SUB-IT'})
SET o.sigla = 'SUB-IT',
    o.nome = 'Itaim Paulista',
    o.endereço = 'Av. Marechal Tito, 3012',
    o.cep = '08160-495',
    o.telefone_fixo = '2572-5400',
    o.grupo_sdwan = 'subitsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'dalmosouza'})
SET r.nome = 'Dalmo Carlos Batista de Souza',
    r.telefone_fixo = '2572-5434',
    r.telefone_movel = '94713-1914',
    r.email = 'dalmosouza@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'josecirsantos'})
SET e1.nome = 'Jocenir Silva Santos',
    e1.email = 'josecirsantos@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-IQ - Itaquera
MERGE (o:OrgaoSetorial {name: 'SUB-IQ'})
SET o.sigla = 'SUB-IQ',
    o.nome = 'Itaquera',
    o.endereço = 'Rua Augusto Carlos Bauman, 851',
    o.cep = '08210-590',
    o.telefone_fixo = '2070-1600',
    o.grupo_sdwan = 'subiqsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'nestorpinto'})
SET r.nome = 'Nestor Pinto',
    r.telefone_fixo = '2070-1623',
    r.telefone_movel = '96812-4678',
    r.email = 'nestorpinto@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'dplima'})
SET e1.nome = 'Djanildo Pedro de Lima',
    e1.telefone_fixo = '2070-1609',
    e1.telefone_movel = '97119-8365',
    e1.email = 'dplima@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'vbastos'})
SET e2.nome = 'Valdir Bastos',
    e2.telefone_fixo = '2070-1605',
    e2.telefone_movel = '97543-1974',
    e2.email = 'vbastos@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o);

// SUB-JA - Jabaquara
MERGE (o:OrgaoSetorial {name: 'SUB-JA'})
SET o.sigla = 'SUB-JA',
    o.nome = 'Jabaquara',
    o.endereço = 'Av. Engenheiro Armando de Arruda Pereira, 2314',
    o.cep = '04309-011',
    o.telefone_fixo = '3397-3200',
    o.grupo_sdwan = 'subjasdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'cvmariano'})
SET r.nome = 'Caue Viera Mariano',
    r.telefone_fixo = '3397-3204',
    r.telefone_movel = '96042-2764',
    r.email = 'cvmariano@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'avsantos'})
SET e1.nome = 'Alexander Victor Paz Santos',
    e1.telefone_fixo = '3397-3224',
    e1.telefone_movel = '97526-7731',
    e1.email = 'avsantos@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'jjesus'})
SET e2.nome = 'Joao Victor Silva Carmo de Jesus',
    e2.telefone_fixo = '3397-3284',
    e2.telefone_movel = '95369-1589',
    e2.email = 'jjesus@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:ESTAGIARIO_TIC_EM]->(o);

// SUB-JT - Jaçanã / Tremembé
MERGE (o:OrgaoSetorial {name: 'SUB-JT'})
SET o.sigla = 'SUB-JT',
    o.nome = 'Jaçanã / Tremembé',
    o.endereço = 'Av. Luis Stamatis, 300',
    o.cep = '02260-000',
    o.telefone_fixo = '3218-4700',
    o.grupo_sdwan = 'subjtsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'decoliveira'})
SET r.nome = 'Douglas Eduardo Caldeira de Oliveira',
    r.telefone_fixo = '3218-4700',
    r.ramal = '4772',
    r.telefone_movel = '99023-5093',
    r.email = 'decoliveira@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'luishsfilho'})
SET e1.nome = 'Luis Henrique da Silva Filho',
    e1.telefone_fixo = '3218-4700',
    e1.ramal = '4772',
    e1.email = 'luishsfilho@smsub.prefeitura.sp.gov.br	'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-LA - Lapa
MERGE (o:OrgaoSetorial {name: 'SUB-LA'})
SET o.sigla = 'SUB-LA',
    o.nome = 'Lapa',
    o.endereço = 'Rua Guaicurus, 1000',
    o.cep = '05033-002',
    o.telefone_fixo = '3396-7500',
    o.grupo_sdwan = 'sublasdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'ccantao'})
SET r.nome = 'Cleiton Luiz Nascimento Cantao',
    r.telefone_fixo = '3396-7551',
    r.telefone_movel = '98279-6769',
    r.email = 'ccantao@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'helmerabvieira'})
SET e1.nome = 'Helmer Augusto Bertolotti Vieira',
    e1.telefone_fixo = '3396-7550',
    e1.email = 'helmerabvieira@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:ESTAGIARIO_TIC_EM]->(o);

// SUB-MB - M Boi Mirim
MERGE (o:OrgaoSetorial {name: 'SUB-MB'})
SET o.sigla = 'SUB-MB',
    o.nome = 'M Boi Mirim',
    o.endereço = 'Av. Guarapiranga, 1695',
    o.cep = '04902-015',
    o.telefone_fixo = '3396-8400',
    o.grupo_sdwan = 'submbsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'ifmenezes'})
SET r.nome = 'Irapuan Farias de Menezes',
    r.telefone_fixo = '3396-8513',
    r.telefone_movel = '97498-1380',
    r.email = 'ifmenezes@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'luanasouza'})
SET e1.nome = 'Luana Gasparini Muniz de Souza',
    e1.telefone_fixo = '3396-8447',
    e1.email = 'luanasouza@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:ESTAGIARIO_TIC_EM]->(o);

// SUB-MO - Moóca
MERGE (o:OrgaoSetorial {name: 'SUB-MO'})
SET o.sigla = 'SUB-MO',
    o.nome = 'Moóca',
    o.endereço = 'Rua Taquari, 549',
    o.cep = '03166-000',
    o.telefone_fixo = '2618-9100',
    o.grupo_sdwan = 'submosdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'emalencar'})
SET r.nome = 'Enio Marcelo Alencar Silva',
    r.telefone_fixo = '2618-9136',
    r.telefone_movel = '99396-9490',
    r.email = 'emalencar@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'bvqueiroz'})
SET e1.nome = 'Bruno Vieira Queiroz',
    e1.telefone_fixo = '2618-9135',
    e1.email = 'bvqueiroz@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:ESTAGIARIO_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'lfbarboza'})
SET e2.nome = 'Luiz Felipe Barboza Machado',
    e2.email = 'lfbarboza@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:ESTAGIARIO_TIC_EM]->(o);

// SUB-PA - Parelheiros
MERGE (o:OrgaoSetorial {name: 'SUB-PA'})
SET o.sigla = 'SUB-PA',
    o.nome = 'Parelheiros',
    o.endereço = 'Av. Sadamu Inoue, 5252',
    o.cep = '04890-380',
    o.telefone_fixo = '5926-6500',
    o.grupo_sdwan = 'subpasdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'ecardozo'})
SET r.nome = 'Emerson da Silva Cardozo',
    r.telefone_fixo = '5926-6504',
    r.ramal = '6504',
    r.telefone_movel = '96052-1027',
    r.email = 'ecardozo@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'cmgil'})
SET e1.nome = 'Carlos Alberto Mariano Gil',
    e1.telefone_fixo = '5926-6560',
    e1.ramal = '6560',
    e1.telefone_movel = '96052-1041',
    e1.email = 'cmgil@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'wkalves'})
SET e2.nome = 'William Klein Hessel Alves',
    e2.telefone_fixo = '5926-6500',
    e2.ramal = '6548',
    e2.telefone_movel = '99439-0501',
    e2.email = 'wkalves@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o);

// SUB-PE - Penha
MERGE (o:OrgaoSetorial {name: 'SUB-PE'})
SET o.sigla = 'SUB-PE',
    o.nome = 'Penha',
    o.endereço = 'Rua Candapuí, 492',
    o.cep = '03621-000',
    o.telefone_fixo = '3397-5100',
    o.grupo_sdwan = 'subpesdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'jsalmeida'})
SET r.nome = 'Joseylton Sales de Almeida',
    r.telefone_fixo = '3397-5238',
    r.telefone_movel = '96730-4576',
    r.email = 'jsalmeida@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o);

// SUB-PR - Perus
MERGE (o:OrgaoSetorial {name: 'SUB-PR'})
SET o.sigla = 'SUB-PR',
    o.nome = 'Perus',
    o.endereço = 'Rua Ylídio Figueiredo, 349',
    o.cep = '05204-020',
    o.telefone_fixo = '3396-8600',
    o.grupo_sdwan = 'subprsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'paulom'})
SET r.nome = 'Paulo Sérgio Monteiro',
    r.telefone_fixo = '3396-8651',
    r.telefone_movel = '96417-5495',
    r.email = 'paulom@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o);

// SUB-PI - Pinheiros
MERGE (o:OrgaoSetorial {name: 'SUB-PI'})
SET o.sigla = 'SUB-PI',
    o.nome = 'Pinheiros',
    o.endereço = 'Avenida Dra Ruth Cardoso, 7123',
    o.cep = '05425-070',
    o.telefone_fixo = '3095-9557',
    o.grupo_sdwan = 'subpisdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'bmluizon'})
SET r.nome = 'Bruno de Melo Luizon dos Santos',
    r.telefone_fixo = '3095-9557',
    r.telefone_movel = '94960-6567',
    r.email = 'bmluizon@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'sebastiaomagalhaes'})
SET e1.nome = 'Sebastião Alves de Magalhães',
    e1.telefone_fixo = '3095-9561',
    e1.email = 'sebastiaomagalhaes@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'pmsilva'})
SET e2.nome = 'Paulo Matias Silva',
    e2.telefone_fixo = '3095-9557',
    e2.email = 'pmsilva@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o);

// SUB-PJ - Pirituba / Jaraguá
MERGE (o:OrgaoSetorial {name: 'SUB-PJ'})
SET o.sigla = 'SUB-PJ',
    o.nome = 'Pirituba / Jaraguá',
    o.endereço = 'Rua Carlos da Cunha Mattos, 67',
    o.cep = '05140-040',
    o.telefone_fixo = '3973-2510',
    o.grupo_sdwan = 'subpjsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'tzachello'})
SET r.nome = 'Túlio César Zachello',
    r.telefone_fixo = '3973-2617',
    r.telefone_movel = '99419-2717',
    r.email = 'tzachello@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'wamoraes'})
SET e1.nome = 'Wierbley Alves de Moraes',
    e1.telefone_fixo = '3973-2612',
    e1.email = 'wamoraes@smsub.prefeitura.sp.gov.br	'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-ST - Santana / Tucuruvi
MERGE (o:OrgaoSetorial {name: 'SUB-ST'})
SET o.sigla = 'SUB-ST',
    o.nome = 'Santana / Tucuruvi',
    o.endereço = 'Av. Tucuruvi, 808',
    o.cep = '02304-002',
    o.telefone_fixo = '2987-3844',
    o.grupo_sdwan = 'substsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'mafmartins'})
SET r.nome = 'Miriam Aparecida Fernandes Martins',
    r.telefone_fixo = '2987-3844',
    r.ramal = '133',
    r.telefone_movel = '95884-6711',
    r.email = 'mafmartins@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o);

// SUB-SA - Santo Amaro
MERGE (o:OrgaoSetorial {name: 'SUB-SA'})
SET o.sigla = 'SUB-SA',
    o.nome = 'Santo Amaro',
    o.endereço = 'Praça Floreano Peixoto, 54',
    o.cep = '04751-030',
    o.telefone_fixo = '3396-6100',
    o.grupo_sdwan = 'subsasdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'alexandresantos'})
SET r.nome = 'Alexandre Pereira dos Santos',
    r.telefone_fixo = '3396-6197',
    r.telefone_movel = '99776-4013',
    r.email = 'alexandresantos@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'lasantos'})
SET e1.nome = 'Luciana Alexandre dos Santos',
    e1.telefone_fixo = '3396-6187',
    e1.email = 'lasantos@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-SB - Sapopemba
MERGE (o:OrgaoSetorial {name: 'SUB-SB'})
SET o.sigla = 'SUB-SB',
    o.nome = 'Sapopemba',
    o.endereço = 'Av. Sapopemba, 9064',
    o.cep = '03988-010',
    o.telefone_fixo = '2701-1400',
    o.ramal = '1402',
    o.grupo_sdwan = 'subsbsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'elianenogueira'})
SET r.nome = 'Eliane da Silva Nogueira',
    r.telefone_fixo = '2701-1468',
    r.email = 'elianenogueira@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:EQUIPE_TIC_EM]->(o);

// SUB-SM - São Mateus
MERGE (o:OrgaoSetorial {name: 'SUB-SM'})
SET o.sigla = 'SUB-SM',
    o.nome = 'São Mateus',
    o.endereço = 'Av. Ragueb Chohfi, 1400',
    o.cep = '08375-000',
    o.telefone_fixo = '3397-1100',
    o.grupo_sdwan = 'subsmsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'lyoshino'})
SET r.nome = 'Lenilson Yoshino Alves',
    r.telefone_fixo = '3397-1116',
    r.telefone_movel = '98204-3167',
    r.email = 'lyoshino@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'vjoliveira'})
SET e1.nome = 'Vagner José de Oliveira',
    e1.email = 'vjoliveira@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-MP - São Miguel Paulista
MERGE (o:OrgaoSetorial {name: 'SUB-MP'})
SET o.sigla = 'SUB-MP',
    o.nome = 'São Miguel Paulista',
    o.endereço = 'Rua Dona Ana Flora Pinheiro de Sousa, 76',
    o.cep = '08060-150',
    o.telefone_fixo = '2030-3720',
    o.grupo_sdwan = 'submpsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'kendi'})
SET r.nome = 'Agnaldo Kendi Kussaba',
    r.telefone_fixo = '2030-3751',
    r.email = 'kendi@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'aparecidodsilva'})
SET e1.nome = 'Aparecido Donizeti da Silva',
    e1.telefone_fixo = '2030-3751',
    e1.email = 'aparecidodsilva@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'fernando'})
SET e2.nome = 'Fernando José Ardezzoni',
    e2.telefone_fixo = '2030-3751',
    e2.email = 'fernando@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o);

// SUB-SE - Sé
MERGE (o:OrgaoSetorial {name: 'SUB-SE'})
SET o.sigla = 'SUB-SE',
    o.nome = 'Sé',
    o.endereço = 'Rua Álvares Penteado, 49',
    o.cep = '01012-001',
    o.telefone_fixo = '3397-1200',
    o.grupo_sdwan = 'subsesdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'cmancini'})
SET r.nome = 'Carlos Roberto Mancini Junior',
    r.telefone_fixo = '3397-1227',
    r.telefone_movel = '98945-4736',
    r.email = 'cmancini@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'varodrigues'})
SET e1.nome = 'Valmir Rodrigues',
    e1.telefone_fixo = '3397-1225',
    e1.email = 'varodrigues@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'danieljoliveira'})
SET e2.nome = 'Daniel Jorge de Oliveira',
    e2.telefone_fixo = '3397-1228',
    e2.email = 'danieljoliveira@smsub.prefeitura.sp.gov.br	'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o);

// SUB-MG - Vila Maria / Vila Guilherme
MERGE (o:OrgaoSetorial {name: 'SUB-MG'})
SET o.sigla = 'SUB-MG',
    o.nome = 'Vila Maria / Vila Guilherme',
    o.endereço = 'Rua General Mendes, 111',
    o.cep = '02127-020',
    o.telefone_fixo = '2967-8100',
    o.grupo_sdwan = 'submgsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'eesantos'})
SET r.nome = 'Eliseu Esau dos Santos',
    r.telefone_fixo = '2967-8100',
    r.ramal = '8081',
    r.telefone_movel = '99328-1998',
    r.email = 'eesantos@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'fernandopsilva'})
SET e1.nome = 'Fernando Pereira da Silva Junior',
    e1.telefone_fixo = '2967-8100',
    e1.ramal = '8082',
    e1.email = 'fernandopsilva@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);

// SUB-VM - Vila Mariana
MERGE (o:OrgaoSetorial {name: 'SUB-VM'})
SET o.sigla = 'SUB-VM',
    o.nome = 'Vila Mariana',
    o.endereço = 'Rua José de Magalhões, 500',
    o.cep = '04026-090',
    o.telefone_fixo = '3397-4100',
    o.grupo_sdwan = 'subvmsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'karakaki'})
SET r.nome = 'Katia Midori Nagamine Arakaki',
    r.telefone_fixo = '3397-4111',
    r.telefone_movel = '98459-6359',
    r.email = 'karakaki@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'gsouto'})
SET e1.nome = 'Gabriel Ferreira Souto',
    e1.telefone_fixo = '3397-4112',
    e1.telefone_movel = '94330-7206',
    e1.email = 'gsouto@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o)

MERGE (e2:Pessoa {name: 'bfcruz'})
SET e2.nome = 'Bernardes Felipe Cruz',
    e2.telefone_fixo = '3397-4112',
    e2.email = 'bfcruz@smsub.prefeitura.sp.gov.br'
MERGE (e2)-[:EQUIPE_TIC_EM]->(o);

// SUB-VP - Vila Prudente
MERGE (o:OrgaoSetorial {name: 'SUB-VP'})
SET o.sigla = 'SUB-VP',
    o.nome = 'Vila Prudente',
    o.endereço = 'Av. do Oratório, 172',
    o.cep = '03220-000',
    o.telefone_fixo = '3397-0800',
    o.grupo_sdwan = 'subvpsdwan@smsub.prefeitura.sp.gov.br'

MERGE (r:Pessoa {name: 'mrcarvalho'})
SET r.nome = 'Miriã Romano Carvalho da Silva',
    r.telefone_fixo = '3397-0841',
    r.telefone_movel = '97288-8812',
    r.email = 'mrcarvalho@smsub.prefeitura.sp.gov.br'
MERGE (r)-[:RESPONSAVEL_TIC_EM]->(o)

MERGE (e1:Pessoa {name: 'almsantos'})
SET e1.nome = 'Antonio Luiz Marinho Santos',
    e1.telefone_fixo = '3397-0853',
    e1.telefone_movel = '98345-4149',
    e1.email = 'almsantos@smsub.prefeitura.sp.gov.br'
MERGE (e1)-[:EQUIPE_TIC_EM]->(o);
