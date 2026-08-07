# Airflow — DAG `atualizar_servicos_sp156`

O Airflow é o **orquestrador** do pipeline SP156 → BookStack. Ele não coleta nem publica nada sozinho importa as funções que fazem esse trabalho e decide **ordem**, **dependência entre etapas** e **quando repetir em caso de falha**.

> A DAG é o que o Airflow chama de "fluxo de trabalho": um conjunto de tarefas (*tasks*) com uma ordem de execução definida.

---

## Sumário

- [Configurar as variáveis do BookStack no Airflow](#configurar-as-variáveis-do-bookstack-no-airflow)
- [Como disparar a DAG](#como-disparar-a-dag)
- [O que a DAG faz](#o-que-a-dag-faz)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Guia de lógica do código](#guia-de-lógica-do-código)
- [Erros mais comuns da DAG](#erros-mais-comuns-da-dag)

---

## Configurar as variáveis do BookStack no Airflow

O pipeline precisa de um Token de API do BookStack para criar/atualizar páginas via API. Esse token **não fica em nenhum `.env`** — ele é cadastrado como **Airflow Variable**, o jeito recomendado pelo próprio Airflow de guardar configuração/segredo que a DAG usa em tempo de execução (dá pra trocar sem subir os containers de novo).

| Passo | Ação |
| :--- | :--- |
| **1** | Acesse `http://bookstack.localhost` com o usuário Administrador → **Meu perfil** → crie um **Token de API**. Copie o **Token ID** e o **Token Secret** — <span style="color:red">o Secret só aparece uma vez, na hora da criação</span> |
| **2** | Acesse o painel do Airflow em `http://airflow.localhost` |
| **3** | No menu superior, navegue até **Admin → Variables** |
| **4** | Adicione duas variáveis: `BOOKSTACK_TOKEN_ID` e `BOOKSTACK_TOKEN_SECRET`, colando os valores copiados no passo 1 |

**Alternativa (variável de ambiente do contêiner):**

```python
import os
token_id = os.environ.get('BOOKSTACK_TOKEN_ID')
token_secret = os.environ.get('BOOKSTACK_TOKEN_SECRET')
```

| Quando usar | Vantagem |
| :--- | :--- |
| **Airflow Variable** | Editável pela interface web, sem redeploy — ideal pra rotacionar o token sem mexer em arquivo nenhum |
| **Variável de ambiente do contêiner** | Definida no `docker-compose.yml`/`.env`, só muda ao subir containers de novo mais rígida, mas fica versionada junto da infra (exceto o valor do segredo em si) |

---

## Como disparar a DAG

1. Acesse `http://airflow.localhost` e faça login com o usuário `admin`.
   > Pra ver a senha gerada automaticamente: `docker exec airflow-webserver_service cat /opt/airflow/simple_auth_manager_passwords.json.generated`
2. No menu superior, clique em **DAGs**.
3. Localize `atualizar_servicos_sp156` na lista.
4. Se o botão ao lado do nome estiver cinza/desligado, clique nele para **ativar** a DAG.
5. Clique no ícone de **(Trigger DAG)**, à direita da linha, e confirme.
6. Acompanhe o progresso clicando no nome da DAG → aba **Grid** ou **Graph**, cada quadrado é uma task (`ajustar_permissoes`, `tabela`, `menu`, `completos`, `publicar`, `backup`).

<span style="color:red"> **Antes de disparar, confirme que o token do BookStack já está cadastrado** (`Admin → Variables` → `BOOKSTACK_TOKEN_ID`/`BOOKSTACK_TOKEN_SECRET`). Sem isso, a DAG roda até a task `publicar` e falha ali.</span>

---

## O que a DAG faz

| Etapa | O que acontece |
| :--- | :--- |
| **1. Ajustar permissões** | Ajusta permissões das pastas compartilhadas (dados/logs usados *durante* a execução) — não confundir com o passo de setup do host (`setup.sh`), que resolve a permissão de `airflow/logs/` antes mesmo do Airflow subir |
| **2. Coletar menu** | Coleta o menu de serviços via Selenium |
| **3. Extrair dados completos** | Abre cada página do menu, uma por vez (sequencial, sem paralelismo, para evitar bloqueio 403), e filtra pelo órgão (SMSUB/SP156/SELIMP) |
| **4. Publicar** | Publica no BookStack (Estante SP156 → Livro por categoria → Capítulo por grupo → Página por serviço), preservando edições manuais via controle de hash |
| **5. Backup** | Faz backup do banco do BookStack (`mariadb-dump`) uma vez por mês, controlando isso numa Airflow Variable — rodar a DAG várias vezes no mesmo mês não repete o dump à toa |

---

## Estrutura de pastas

O projeto separa **o que é DAG** do **que é código auxiliar** uma boa prática comum em projetos Airflow, que evita que o `dag-processor` (o processo que fica escaneando pastas em busca de DAGs) perca performance ou se confunda tentando interpretar arquivos que não são DAGs.

| Pasta | Conteúdo |
| :--- | :--- |
| **`airflow/dags/`** | Exclusivamente arquivos `.py` que definem DAGs (neste projeto, só `atualizar_servicos_sp156.py`). Nada de função auxiliar, script de coleta ou lógica de negócio aqui dentro |
| **`bookstack/include/`** | Scripts de ETL e código auxiliar (`coleta.py`, `hash_bookstack.py`, `bookstack_publicacao.py`, `backup_bookstack.py`). É daqui que a DAG importa as funções que ela orquestra |

<span style="color:red"> **Nota de local físico:** o padrão comum em projetos Airflow chamaria essa segunda pasta de `airflow/include/`. Neste projeto ela fica fisicamente em `bookstack/include/` é o caminho real montado no `docker-compose.yml`. A DAG importa de lá normalmente, sem diferença de comportamento.</span>

O **`PYTHONPATH=/opt/airflow`** (configurado no `docker-compose.yml`, dentro do bloco `x-airflow-common`) diz ao Python para procurar módulos a partir da raiz `/opt/airflow`, onde `dags/` e `include/` são montados dentro do container. Por causa disso, a DAG importa assim:

```python
from include.coleta import pegar_menu, completar_dados
from include.bookstack_publicacao import publicar_no_bookstack
from include.hash_bookstack import garantir_tabela
from include.backup_bookstack import fazer_backup
```

> Se criar um novo módulo auxiliar, ele vai em `bookstack/include/` e é importado como `from include.seu_modulo import sua_funcao` — não precisa mexer em `PYTHONPATH` nem no `docker-compose.yml`.

---

## Guia de lógica do código

### 1. `coleta.py`

Busca os dados no site do SP156. Não sabe nada sobre BookStack ou banco, só coleta e salva em JSON. 3 etapas, cada uma com checkpoint próprio (retoma de onde parou, não do zero).

| Função | O que faz | Por quê |
| :--- | :--- | :--- |
| `HEADERS` | Finge ser um navegador real | Sem isso, a proteção anti-bot bloqueia e o pipeline "roda", mas não extrai nada |
| `orgao_e_da_smsub` | Filtra só SMSUB/SELIMP | O site lista várias secretarias |
| `campos_da_pagina` | Extrai "O que é", "Prazo máximo", etc., preservando link e parágrafo (marcadores invisíveis `MARCADOR_LINK_*`/`MARCADOR_PARAGRAFO`) | Lê o texto corrido (não linha a linha) porque o site fragmenta títulos em vários `<span>`; sem os marcadores, `get_text()` apagava todo `<a>`/`<p>` original |
| `pegar_menu` | Navega o menu via Selenium | Serve como checkpoint por categoria |
| `pausa_entre_requisicoes` | Pausa aleatória antes de cada request | Sem isso, workers em paralelo martelam o site e ele bloqueia em massa (caso real: 602/615 páginas bloqueadas) |
| `varrer_ids` | Testa faixa de IDs 700–7000 em paralelo | Acha páginas "órfãs" que não aparecem no menu; checkpoint por mini-lote de 100. <span style="color:red">**Não é chamada pela DAG atualmente** o código continua no arquivo, mas foi removida do pipeline por gerar bloqueio 403 excessivo</span> |
| `completar_dados` | Extrai conteúdo completo + aplica filtro de órgão, sequencial (sem paralelismo) | Tem trava de segurança: se a maioria das páginas vier "sem conteúdo" ou for tudo bloqueio, falha de propósito em vez de publicar quase vazio (já aconteceu: 1/615 por causa de captcha) |

**Próximo elo da cadeia:** salva `dados_completos.json` é o que `bookstack_publicacao.py` lê pra saber o que publicar.

---

### 2. `hash_bookstack.py`

Responde: **"esse conteúdo mudou de verdade desde a última vez?"** Sem isso, toda execução reescreveria tudo, mesmo sem mudança, e apagaria edições manuais feitas direto no BookStack.

| Função | O que faz | Por quê |
| :--- | :--- | :--- |
| `hash_de_conteudo` | Normaliza o texto (tira espaço duplicado/quebra de linha) e gera um SHA-256 | Mesma vírgula a mais → hash igual; conteúdo diferente → hash diferente |
| `_conectar` | Abre conexão nova a cada chamada | Tasks do Airflow rodam em processos separados, conexão de um processo não serve pro outro |
| `decidir_acao` | Função pura (sem I/O). Checa **primeiro** se a página foi editada manualmente no BookStack, independente da fonte ter mudado, e só depois compara com a fonte | Garante que edição manual sempre tenha prioridade sobre mudança na fonte |
| `recalibrar_todas_hash_publicado` | Migração pontual (rodar manualmente, uma vez só, nunca como parte da DAG): recalcula o `hash_publicado` a partir do HTML que o BookStack realmente guarda | Corrige o descompasso causado pelo BookStack reprocessar/reformatar o HTML ao salvar |

**`decidir_acao` devolve uma das 4 ações abaixo:**

| Ação | Quando acontece |
| :--- | :--- |
| **CRIAR** | Nunca vimos essa página, ou ela "sumiu" do BookStack |
| **PULAR** | Fonte não mudou, a página ainda existe, e ninguém editou por fora |
| **CONFLITO** | Alguém editou a página no BookStack por fora do robô checado independente da fonte ter mudado |
| **ATUALIZAR** | Fonte mudou e ninguém mexeu manualmente |

> Quando dá **CONFLITO**, quem resolve é uma pessoa, direto na página do BookStack, usando as tags `sp156_aprovado`/`sp156_rejeitado` — isso está documentado no `README.md` do BookStack, não aqui, porque é uma ação de interface, não de código.

**Próximo elo da cadeia:** `bookstack_publicacao.py` importa `decidir_acao` ele não decide sozinho, pergunta pra esse arquivo.

---

### 3. `bookstack_publicacao.py`

Fala com a API do BookStack. Hierarquia: **Estante → Livro → Capítulo → Página**.

| Função | O que faz | Por quê |
| :--- | :--- | :--- |
| `_obter_ou_criar` | Padrão *get or create*: procura pelo nome, cria só se não achar. Usado pra Estante/Livro/Capítulo | Evita duplicar hierarquia a cada execução |
| `_pagina_compativel_com_tipo` / `_pagina_compativel_com_codigo` | Guarda contra duas páginas com o mesmo nome (ex: "Fazer reclamação" se repete em várias categorias) | Sem isso, a segunda sobrescreveria o conteúdo da primeira silenciosamente |
| `texto_de_campo_para_html` / `_linkificar` | Convertem os marcadores de link/parágrafo vindos de `coleta.py` em `<p>` e `<a>` de verdade | Reconstrói a formatação original perdida na extração |
| `criar_atualizar` | Cria/atualiza a página via API e **busca ela de volta** (GET) logo em seguida | O BookStack reprocessa o HTML ao salvar hashear o que foi enviado nunca bateria com uma leitura futura |
| `_resolucao_de_conflito` | Lê as tags `sp156_aprovado`/`sp156_rejeitado` que um humano coloca manualmente na página | Resolve um conflito sem precisar mexer em código |
| `CONTADOR_POR_STATUS` / `ROTULO_ACAO_EVENTO` | Dicionários de "tradução" (status técnico → nome do contador / texto de exibição) | Centraliza a tradução num lugar só, em vez de espalhar `if status == ...` pelo código |
| `publicar_no_bookstack(arquivo, apenas_um=False)` | Função principal chamada pela DAG. `apenas_um=True` processa só a primeira categoria (uso só em teste, não em produção). Devolve um dicionário-resumo (`paginas_criadas`, `paginas_atualizadas`, etc.) | É esse resumo que aparece no log da task no Airflow |

**Próximo elo da cadeia:** depois de publicar tudo, o pipeline segue pro backup — faz sentido fazer isso **depois**, pra capturar o conteúdo mais recente.

---

### 4. `backup_bookstack.py`

O mais simples de todos: dump do MariaDB → `.gz` → apaga backups antigos. Sem paralelismo, sem checkpoint (roda 1x por mês).

| Função | O que faz | Por quê |
| :--- | :--- | :--- |
| `_rodar_mariadb_dump` | Se falhar, apaga o `.sql` parcial | Evita backup corrompido disfarçado de válido |
| `_apagar_backups_antigos` | Nome do arquivo tem timestamp, então ordenar por nome já ordena por data. Mantém só os `MANTER_ULTIMOS_PADRAO` (14) mais recentes | Evita acúmulo indefinido de arquivos de backup |
| `fazer_backup` | Junta os dois passos acima e devolve o caminho do arquivo gerado | Ponto de entrada usado pela DAG |

**Próximo elo da cadeia:** não alimenta nenhum outro arquivo. Quem decide *quando* chamar (regra de "1x por mês") é a DAG.

---

### 5. `atualizar_servicos_sp156.py` — a DAG em si

Não faz trabalho pesado sozinha importa os 4 arquivos acima e define **ordem** e **regras** de quando cada um roda.

| Ponto-chave | Explicação |
| :--- | :--- |
| Tasks não trocam dado em memória | Cada uma escreve num JSON em disco (`PASTA_DADOS`/`ARQ_*`), a próxima lê é assim que `coleta.py` "conversa" com `bookstack_publicacao.py` |
| `_var_int` | Lê uma Airflow Variable (configurável na interface, sem redeploy) como inteiro, com valor padrão |
| `schedule=None` | Não roda sozinha só quando disparada manualmente |
| `max_active_runs=1` | Impede duas execuções ao mesmo tempo (evitaria coletar em duplicidade e causar mais bloqueio) |
| `backup_bookstack_task` | Só chama `fazer_backup()` se o mês mudou desde o último backup salvo numa Airflow Variable é assim que "mensal" é implementado mesmo a DAG rodando várias vezes no mês |
| `ajustar_permissoes >> tabela >> menu >> completos >> publicar >> backup` | O `>>` significa **"depende de"** cada task só começa depois que a anterior termina com sucesso |

---

**Fechando o ciclo:**

```
coleta.py → dados_completos.json
          → hash_bookstack.py decide a ação
          → bookstack_publicacao.py publica
          → backup_bookstack.py faz o dump

atualizar_servicos_sp156.py amarra os 4 arquivos acima numa sequência.
```

---

## Erros mais comuns da DAG

| Sintoma | Causa provável | O que fazer |
| :--- | :--- | :--- |
| `dag-processor` reinicia sozinho / DAG não aparece na interface | Permissão de pasta | Rode `bash setup.sh` de novo (na raiz do projeto), ele reajusta as permissões antes de subir |
| Airflow sobe mas fica **unhealthy** | Postgres (metastore do Airflow) ainda inicializando | Espere ~60s (o `start_period` do healthcheck) antes de considerar que travou de verdade |
| DAG dispara mas falha na task `publicar` | Token do BookStack não cadastrado, ou expirado | Confira `Admin → Variables` → `BOOKSTACK_TOKEN_ID`/`BOOKSTACK_TOKEN_SECRET` |
| `completar_dados` falha de propósito, com `RuntimeError` | Trava de segurança ativada: maioria das páginas veio bloqueada/vazia | Não é bug é o comportamento esperado. Verifique se o site SP156 está bloqueando o IP do container (rate limit) antes de tentar de novo |
| Muitas páginas em `CONFLITO` no log da task `publicar` | Alguém editou manualmente várias páginas no BookStack | Resolva uma a uma com as tags `sp156_aprovado`/`sp156_rejeitado`, direto no BookStack (ver README do BookStack) |

> Erros de infraestrutura (porta ocupada, container não sobe, certificado HTTPS) não são específicos do Airflow — consulte o README principal do projeto.