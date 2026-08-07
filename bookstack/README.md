# BookStack

Wiki onde o pipeline SP156 publica os serviços e informativos da SMSUB/SELIMP automaticamente. Também é editável manualmente por pessoas com perfil de Editor.

![Fluxograma do projeto](bookstack/assets/vertical-bookstack.png)

> A coleta, o controle de versão do conteúdo e a publicação são feitos pelo **Airflow** veja o `README.md` da pasta `airflow/` para entender a DAG e a lógica do pipeline. Este README aqui é só sobre o BookStack em si: acesso, perfis e o que fazer quando o robô e uma edição manual entram em conflito.

---

## Sumário

- [Acesso](#acesso)
- [Criar perfil de Editor](#criar-perfil-de-editor)
- [Deixar o conteúdo público](#deixar-o-conteúdo-público)
- [Tags para autorizar ou negar a edição manual](#tags-para-autorizar-ou-negar-a-edição-manual)
- [Personalizar a aparência](#personalizar-a-aparência)

---

## Acesso

| Endereço | Credenciais |
| :--- | :--- |
| http://bookstack.localhost | `admin@admin.com` / `password` |

<span style="color:red">⚠️ Troque a senha do admin no primeiro acesso, principalmente se o ambiente for exposto além de `localhost`.</span>

---

## Criar perfil de Editor

Por padrão só o Administrador pode editar. Pra dar acesso de edição pra outra pessoa, sem dar acesso total de administração:

**Com o perfil de Administrador:**

1. **Configurações → Perfis** → selecione: *Gerenciar todos os livros, capítulos e permissões de páginas* / *Gerenciar os modelos de página* / *Exportar conteúdo* / *Importar conteúdo*.
2. Em **Permissões de Ativos**, selecione tudo.
3. **Usuários → Adicionar novo usuário** → preencha nome e e-mail → marque a caixa **Editor** → desmarque "enviar por e-mail" e defina uma senha diretamente.
4. Entre com o perfil de Editor criado.

---

## Deixar o conteúdo público

Pra permitir visualização/exportação sem login: **Configurações → Acesso Público**, marque a caixa.

---

## Tags para autorizar ou negar a edição manual

O pipeline do Airflow detecta quando uma página foi editada manualmente (fora do robô) e marca isso como **CONFLITO** ele para de sobrescrever essa página sozinho até alguém decidir o que fazer. Essa decisão é tomada aqui, com uma tag, direto na página:

1. Pegue o código do serviço e vá até a página correspondente.
2. Clique em **Editar** → na lateral direita, clique em **Editar** de novo → uma barra lateral vai abrir.
3. Clique no segundo ícone → **Adicionar outro marcador**.
4. Preencha o campo **"Nome do marcador"** com uma das duas opções:

| Marcador | Efeito |
| :--- | :--- |
| `sp156_rejeitado` | Restaura o conteúdo oficial (descarta a edição manual) |
| `sp156_aprovado` | Mantém a edição manual (ignora a fonte oficial) |

<span style="color:red">⚠️ **Só o nome do marcador importa** o campo "Valor do marcador" pode ficar em branco.</span>

---

## Personalizar a aparência

Veja o [Guia de Estilo](bookstack/assets/css_bookstack.md).