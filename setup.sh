#!/bin/bash
set -e

# Cores para melhor visualização
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# BLOCO 1 — Lista dos arquivos de senha (.env)
ARQUIVOS_ENV=(
    "airflow/.env"
    "bookstack/.env"
    "mariadb/.env"
    "neo4j/.env"
    "fastapi/.env"
    "streamlit/.env"
)

# BLOCO 2 — Definição dos GRUPOS de serviços
declare -A GRUPOS_SERVICOS

GRUPOS_SERVICOS["airflow"]="airflow-init airflow-webserver airflow-scheduler airflow-dag-processor"
GRUPOS_SERVICOS["database"]="mariadb_service postgres"
GRUPOS_SERVICOS["neo4j"]="neo4j neo4j-init"
GRUPOS_SERVICOS["bookstack"]="bookstack"
GRUPOS_SERVICOS["fastapi"]="fastapi"
GRUPOS_SERVICOS["nginx"]="nginx"
GRUPOS_SERVICOS["streamlit"]="streamlit"

# BLOCO 3 — Lista de todos os serviços (para referência)
TODOS_SERVICOS=(
    "mariadb_service"
    "postgres"
    "neo4j"
    "neo4j-init"
    "bookstack"
    "fastapi"
    "airflow-init"
    "airflow-webserver"
    "airflow-scheduler"
    "airflow-dag-processor"
    "nginx"
    "streamlit"
)

# BLOCO 4 — Função para obter serviços de um grupo
get_servicos_do_grupo() {
    local grupo="$1"
    echo "${GRUPOS_SERVICOS[$grupo]}"
}

# ============================================
# BLOCO 5 — Função para validar se os .env estão preenchidos
# ============================================
validar_env_preenchido() {
    local arquivo="$1"
    local variaveis_obrigatorias=("$@")
    local faltando=()
    
    # Remove o primeiro argumento (nome do arquivo)
    shift
    
    for var in "$@"; do
        if ! grep -q "^${var}=" "$arquivo" 2>/dev/null; then
            faltando+=("$var")
        else
            # Verifica se a variável tem valor (não está vazia)
            local valor=$(grep "^${var}=" "$arquivo" | cut -d= -f2-)
            if [ -z "$valor" ]; then
                faltando+=("$var (vazio)")
            fi
        fi
    done
    
    if [ ${#faltando[@]} -gt 0 ]; then
        return 1
    fi
    return 0
}

# ============================================
# BLOCO 6 — Função para verificar se os .env estão completos
# ============================================
verificar_envs_completos() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}        VERIFICANDO ARQUIVOS .env                         ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    local ENV_FALTANDO=()
    local ENV_SEM_VALORES=()
    local ENV_OK=()
    local TODOS_PREENCHIDOS=true
    
    # Verifica cada arquivo .env
    for arquivo in "${ARQUIVOS_ENV[@]}"; do
        if [ ! -f "$arquivo" ]; then
            ENV_FALTANDO+=("$arquivo")
            TODOS_PREENCHIDOS=false
            continue
        fi
        
        # Verifica se tem variáveis preenchidas
        if grep -q "=" "$arquivo" 2>/dev/null; then
            # Verifica se as variáveis principais estão preenchidas
            local TEM_VALOR=false
            while IFS= read -r linha; do
                if [[ "$linha" =~ ^[A-Z_]+= ]] && [ -n "$(echo "$linha" | cut -d= -f2-)" ]; then
                    TEM_VALOR=true
                    break
                fi
            done < "$arquivo"
            
            if [ "$TEM_VALOR" = true ]; then
                ENV_OK+=("$arquivo")
            else
                ENV_SEM_VALORES+=("$arquivo")
                TODOS_PREENCHIDOS=false
            fi
        else
            ENV_SEM_VALORES+=("$arquivo")
            TODOS_PREENCHIDOS=false
        fi
    done
    
    # Mostra resumo
    if [ ${#ENV_OK[@]} -gt 0 ]; then
        echo -e "${GREEN}  Arquivos .env completos:${NC}"
        for arquivo in "${ENV_OK[@]}"; do
            echo "  - $arquivo"
        done
    fi
    
    if [ ${#ENV_SEM_VALORES[@]} -gt 0 ]; then
        echo -e "${YELLOW}  Arquivos .env sem valores preenchidos:${NC}"
        for arquivo in "${ENV_SEM_VALORES[@]}"; do
            echo "  - $arquivo"
        done
    fi
    
    if [ ${#ENV_FALTANDO[@]} -gt 0 ]; then
        echo -e "${RED}  Arquivos .env faltando:${NC}"
        for arquivo in "${ENV_FALTANDO[@]}"; do
            echo "  - $arquivo"
        done
    fi
    
    echo ""
    
    if [ "$TODOS_PREENCHIDOS" = true ]; then
        echo -e "${GREEN}  Todos os arquivos .env estão preenchidos!${NC}"
        return 0
    else
        echo -e "${YELLOW}  Alguns arquivos .env precisam ser preenchidos.${NC}"
        return 1
    fi
}

# ============================================
# BLOCO 7 — Função para validar senha do MariaDB
# ============================================
validar_senha_mariadb() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}        VALIDANDO SENHA DO MARIADB                       ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Carrega a senha do mariadb/.env
    if [ -f "./mariadb/.env" ]; then
        set -a
        source ./mariadb/.env
        set +a
    else
        echo -e "${RED}  Arquivo mariadb/.env não encontrado!${NC}"
        return 1
    fi
    
    # Verifica se a senha está definida
    if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
        echo -e "${YELLOW}  Senha do MariaDB não definida em mariadb/.env${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}  Verificando se a senha do MariaDB está correta...${NC}"
    
    # Verifica se o container existe
    if docker ps -a --format '{{.Names}}' | grep -q "mariadb_service"; then
        # Container existe, tenta validar a senha
        if docker compose exec -T mariadb_service \
            mariadb -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1;" > /dev/null 2>&1; then
            echo -e "${GREEN}  Senha do MariaDB validada com sucesso!${NC}"
            return 0
        else
            echo -e "${RED}  Senha do MariaDB incorreta!${NC}"
            echo -e "${YELLOW}   A senha em mariadb/.env não bate com o banco.${NC}"
            return 1
        fi
    else
        # Container não existe, não podemos validar
        echo -e "${YELLOW}  Container MariaDB não está rodando. Não é possível validar a senha.${NC}"
        echo -e "${YELLOW}   Vamos iniciar o MariaDB e validar depois.${NC}"
        return 2
    fi
}

# ============================================
# BLOCO 8 — Função para perguntar se quer regerar
# ============================================
perguntar_regerar() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}        CONFIGURAÇÃO DE SEGREDOS                         ${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Deseja regerar as senhas e chaves?${NC}"
    echo -e "  ${GREEN}1${NC}) Manter as senhas existentes (recomendado)"
    echo -e "  ${YELLOW}2${NC}) Regerar todas as senhas e chaves"
    echo -e "  ${RED}3${NC}) Sair"
    echo ""
    read -rp "Digite 1, 2 ou 3: " OPCAO_REGERAR
    
    case "$OPCAO_REGERAR" in
        1)
            echo ""
            echo -e "${GREEN}  Mantendo senhas existentes.${NC}"
            return 0
            ;;
        2)
            echo ""
            echo -e "${YELLOW}  Regerando todas as senhas e chaves...${NC}"
            return 1
            ;;
        3)
            echo ""
            echo -e "${RED}Saindo...${NC}"
            exit 0
            ;;
        *)
            echo ""
            echo -e "${RED} Opção inválida!${NC}"
            sleep 1
            perguntar_regerar
            return $?
            ;;
    esac
}

# ============================================
# BLOCO 9 — Função para subir containers com opção de cancelar
# ============================================
subir_com_cancelamento() {
    local SERVICOS=("$@")
    
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}        PREPARANDO PARA SUBIR CONTAINERS                 ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${GREEN}Containers que serão iniciados:${NC}"
    for servico in "${SERVICOS[@]}"; do
        echo "  - $servico"
    done
    echo ""
    
    echo -e "${YELLOW}Opções:${NC}"
    echo "  ${GREEN}1${NC}) Confirmar e subir"
    echo "  ${RED}2${NC}) Cancelar e voltar"
    echo "  ${YELLOW}3${NC}) Ver detalhes dos containers"
    echo ""
    read -rp "Digite 1, 2 ou 3: " OPCAO_FINAL
    
    case "$OPCAO_FINAL" in
        1)
            echo ""
            echo -e "${GREEN}  Iniciando containers...${NC}"
            echo -e "${YELLOW}Pressione 'c' a qualquer momento para cancelar${NC}"
            echo ""
            
            # Executa em background para permitir cancelamento
            docker compose up -d "${SERVICOS[@]}" &
            PID=$!
            
            # Loop para monitorar e permitir cancelamento
            while kill -0 $PID 2>/dev/null; do
                echo -ne "\r${YELLOW}  Subindo containers... (digite 'c' para cancelar)${NC} "
                read -t 1 -n 1 COMANDO 2>/dev/null || true
                if [ "$COMANDO" = "c" ] || [ "$COMANDO" = "C" ]; then
                    echo ""
                    echo -e "${RED}  Cancelando subida dos containers...${NC}"
                    kill $PID 2>/dev/null
                    wait $PID 2>/dev/null
                    echo -e "${YELLOW}🔙 Voltando ao menu de seleção!${NC}"
                    sleep 2
                    return 1
                fi
            done
            
            wait $PID
            echo ""
            echo -e "${GREEN}  Containers iniciados com sucesso!${NC}"
            docker compose ps
            return 0
            ;;
        2)
            echo ""
            echo -e "${YELLOW}🔙 Cancelando e voltando ao menu...${NC}"
            sleep 1
            return 1
            ;;
        3)
            echo ""
            echo -e "${BLUE}Detalhes dos containers selecionados:${NC}"
            for servico in "${SERVICOS[@]}"; do
                echo ""
                echo -e "${GREEN}  $servico${NC}"
                docker compose config 2>/dev/null | grep -A 20 "^  $servico:" || true
            done
            echo ""
            # Volta para a confirmação
            subir_com_cancelamento "${SERVICOS[@]}"
            return $?
            ;;
        *)
            echo ""
            echo -e "${RED}  Opção inválida!${NC}"
            sleep 1
            subir_com_cancelamento "${SERVICOS[@]}"
            return $?
            ;;
    esac
}

# ============================================
# BLOCO 10 — Função para selecionar containers com navegação
# ============================================
selecionar_containers() {
    local SERVICOS_SELECIONADOS=()
    
    while true; do
        clear
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}        SELECIONE OS CONTAINERS PARA SUBIR                ${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}        GRUPOS DISPONÍVEIS                               ${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        
        GRUPOS=("airflow" "database" "neo4j" "bookstack" "fastapi" "nginx" "streamlit")
        
        for i in "${!GRUPOS[@]}"; do
            SERVICOS=$(get_servicos_do_grupo "${GRUPOS[$i]}")
            echo -e "  ${GREEN}$((i+1))${NC}) ${BLUE}${GRUPOS[$i]}${NC} → $SERVICOS"
        done
        
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}        OU SELECIONE INDIVIDUALMENTE                     ${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        
        for i in "${!TODOS_SERVICOS[@]}"; do
            echo -e "  ${YELLOW}$((i+11))${NC}) ${TODOS_SERVICOS[$i]}"
        done
        
        echo ""
        echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${MAGENTA}        COMANDOS ESPECIAIS                              ${NC}"
        echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "  ${GREEN}0${NC}) ${BLUE}TODOS${NC} os containers"
        echo -e "  ${YELLOW}r${NC}) ${RED}Reiniciar${NC} seleção (limpar tudo)"
        echo -e "  ${YELLOW}v${NC}) ${BLUE}Voltar${NC} ao menu principal"
        echo ""
        
        if [ ${#SERVICOS_SELECIONADOS[@]} -gt 0 ]; then
            echo -e "${GREEN}  Containers já selecionados (${#SERVICOS_SELECIONADOS[@]}):${NC}"
            for svc in "${SERVICOS_SELECIONADOS[@]}"; do
                echo "  - $svc"
            done
            echo ""
            echo -e "${GREEN}s${NC}) ${GREEN}Confirmar${NC} seleção (ir para subida)"
        fi
        
        echo ""
        read -rp "Digite sua escolha: " ESCOLHA
        
        case "$ESCOLHA" in
            0)
                echo ""
                echo -e "${GREEN}  Todos os containers selecionados!${NC}"
                SERVICOS_SELECIONADOS=("${TODOS_SERVICOS[@]}")
                return 0
                ;;
            r|R)
                SERVICOS_SELECIONADOS=()
                echo ""
                echo -e "${YELLOW}  Seleção reiniciada!${NC}"
                sleep 1
                continue
                ;;
            v|V)
                echo ""
                echo -e "${YELLOW}  Voltando ao menu principal...${NC}"
                sleep 1
                return 1
                ;;
            s|S)
                if [ ${#SERVICOS_SELECIONADOS[@]} -gt 0 ]; then
                    echo ""
                    echo -e "${GREEN}  Confirmando seleção...${NC}"
                    return 0
                else
                    echo ""
                    echo -e "${RED}  Nenhum container selecionado!${NC}"
                    sleep 1
                    continue
                fi
                ;;
        esac
        
        if [[ "$ESCOLHA" =~ ^[0-9]+$ ]]; then
            NUMERO=$ESCOLHA
            
            if [ "$NUMERO" -ge 1 ] && [ "$NUMERO" -le 6 ]; then
                GRUPO="${GRUPOS[$((NUMERO-1))]}"
                SERVICOS_DO_GRUPO=$(get_servicos_do_grupo "$GRUPO")
                
                JA_SELECIONADO="false"
                for svc in $SERVICOS_DO_GRUPO; do
                    if [[ " ${SERVICOS_SELECIONADOS[*]} " =~ " $svc " ]]; then
                        JA_SELECIONADO="true"
                    fi
                done
                
                if [ "$JA_SELECIONADO" = "true" ]; then
                    echo ""
                    echo -e "${YELLOW}  Grupo '${GRUPO}' já selecionado!${NC}"
                    sleep 1
                else
                    for svc in $SERVICOS_DO_GRUPO; do
                        SERVICOS_SELECIONADOS+=("$svc")
                    done
                    echo ""
                    echo -e "${GREEN}✓${NC} Grupo '${GRUPO}' adicionado!"
                    sleep 1
                fi
                continue
            fi
            
            if [ "$NUMERO" -ge 7 ] && [ "$NUMERO" -le $((6 + ${#TODOS_SERVICOS[@]})) ]; then
                IDX=$((NUMERO-7))
                SERVICO="${TODOS_SERVICOS[$IDX]}"
                
                if [[ " ${SERVICOS_SELECIONADOS[*]} " =~ " $SERVICO " ]]; then
                    echo ""
                    echo -e "${YELLOW}  Container '$SERVICO' já selecionado!${NC}"
                    sleep 1
                else
                    SERVICOS_SELECIONADOS+=("$SERVICO")
                    echo ""
                    echo -e "${GREEN}✓${NC} Container '$SERVICO' adicionado!"
                    sleep 1
                fi
                continue
            fi
            
            echo ""
            echo -e "${RED}  Número inválido: $NUMERO${NC}"
            sleep 1
        else
            echo ""
            echo -e "${RED}  Opção inválida!${NC}"
            sleep 1
        fi
    done
}

# ============================================
# BLOCO 11 — Função para mostrar o menu principal
# ============================================
menu_principal() {
    clear
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}        SETUP - PROJETO GOVERNANÇA TIC                    ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}Escolha uma opção:${NC}"
    echo ""
    echo -e "  ${GREEN}1${NC}) Subir todos os containers"
    echo -e "  ${GREEN}2${NC}) Escolher containers específicos"
    echo -e "  ${GREEN}3${NC}) Verificar status dos containers"
    echo -e "  ${RED}4${NC}) Sair"
    echo ""
    read -rp "Digite 1, 2, 3 ou 4: " OPCAO
    
    case "$OPCAO" in
        1)
            echo ""
            echo -e "${GREEN}Subindo todos os containers...${NC}"
            if subir_com_cancelamento "${TODOS_SERVICOS[@]}"; then
                return 0
            else
                return 1
            fi
            ;;
        2)
            if selecionar_containers; then
                local SERVICOS_PARA_SUBIR=("${SERVICOS_SELECIONADOS[@]}")
                SERVICOS_PARA_SUBIR=($(echo "${SERVICOS_PARA_SUBIR[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))
                
                if [ ${#SERVICOS_PARA_SUBIR[@]} -eq 0 ]; then
                    echo -e "${RED}  Nenhum container selecionado. Voltando...${NC}"
                    sleep 1
                    return 1
                fi
                
                echo ""
                echo -e "${YELLOW}Deseja subir também os containers dos quais eles dependem?${NC}"
                echo "  1) Sim - Subir com dependências (recomendado)"
                echo "  2) Não - Subir apenas os selecionados"
                echo ""
                read -rp "Digite 1 ou 2: " OPCAO_DEPENDENCIAS
                
                if [ "$OPCAO_DEPENDENCIAS" = "1" ]; then
                    echo ""
                    echo -e "${GREEN}Subindo containers selecionados com dependências...${NC}"
                    if subir_com_cancelamento "${SERVICOS_PARA_SUBIR[@]}"; then
                        return 0
                    else
                        return 1
                    fi
                else
                    echo ""
                    echo -e "${YELLOW}  Subindo apenas os containers selecionados (sem dependências)${NC}"
                    if subir_com_cancelamento "${SERVICOS_PARA_SUBIR[@]}"; then
                        return 0
                    else
                        return 1
                    fi
                fi
            else
                return 1
            fi
            ;;
        3)
            echo ""
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${BLUE}        STATUS DOS CONTAINERS                           ${NC}"
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            docker compose ps
            echo ""
            read -rp "Pressione ENTER para continuar..."
            return 1
            ;;
        4)
            echo ""
            echo -e "${RED}Saindo...${NC}"
            exit 0
            ;;
        *)
            echo ""
            echo -e "${RED}  Opção inválida!${NC}"
            sleep 1
            return 1
            ;;
    esac
}

# ============================================
# BLOCO 12 — Função de Retry
# ============================================
tentar_com_retry() {
    local descricao="$1"
    shift

    local tentativas=3
    local espera=15
    local n=1

    until "$@"; do
        if [ "$n" -ge "$tentativas" ]; then
            echo -e "${RED}  $descricao falhou após $tentativas tentativas.${NC}"
            return 1
        fi

        echo -e "${YELLOW}  $descricao falhou (tentativa $n/$tentativas). Esperando ${espera}s e tentando de novo...${NC}"
        sleep "$espera"
        n=$((n + 1))
    done
}

# ============================================
# INÍCIO DA EXECUÇÃO PRINCIPAL
# ============================================

# BLOCO 13 — Monta dinamicamente as flags --env-file
FLAGS_ENV_FILE=()

for arquivo in "${ARQUIVOS_ENV[@]}"; do
    FLAGS_ENV_FILE+=(--env-file "$arquivo")
done

# BLOCO 14 — Verifica se os .env existem e estão preenchidos
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}        INICIANDO SETUP                                   ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Verifica se os .env existem, se não, cria a partir do .example
for arquivo in "${ARQUIVOS_ENV[@]}"; do
    if [ ! -f "$arquivo" ]; then
        echo -e "${YELLOW}  $arquivo não encontrado - copiando de ${arquivo}.example...${NC}"
        cp "${arquivo}.example" "$arquivo"
    fi
done

# Verifica se os .env estão completos
if verificar_envs_completos; then
    echo -e "${GREEN}  Todos os arquivos .env estão prontos!${NC}"
    
    # Valida a senha do MariaDB
    validar_senha_mariadb
    RESULTADO_VALIDACAO=$?
    
    if [ $RESULTADO_VALIDACAO -eq 1 ]; then
        # Senha incorreta, pergunta se quer regerar
        echo ""
        echo -e "${RED}  A senha do MariaDB está incorreta!${NC}"
        if perguntar_regerar; then
            echo -e "${GREEN}  Mantendo senhas existentes. Vamos tentar iniciar o MariaDB...${NC}"
        else
            FORCAR_REGERACAO="true"
        fi
    fi
else
    echo -e "${YELLOW}  Alguns arquivos .env precisam ser preenchidos.${NC}"
    echo -e "${YELLOW}   Vamos gerar novas senhas e chaves.${NC}"
    FORCAR_REGERACAO="true"
    E_PRIMEIRO_BOOT="true"
fi

echo ""

# BLOCO 15 — Carrega os .env
for arquivo in "${ARQUIVOS_ENV[@]}"; do
    set -a
    source "$arquivo"
    set +a
done

# BLOCO 16 — Decide se vai REGERAR os segredos ou manter os antigos
if [ "$1" = "--regerar-segredos" ]; then
    FORCAR_REGERACAO="true"
    echo -e "${YELLOW}  Modo --regerar-segredos ativado: valores existentes serão sobrescritos.${NC}"
    echo ""
fi

# Verifica se o volume do MariaDB já existe no Docker
if ! docker volume ls --format '{{.Name}}' | grep -qE '(^|_)mariadb_data$'; then
    echo -e "${YELLOW}Nenhum volume de dados encontrado — ambiente do zero. Segredos serão gerados novos.${NC}"
    FORCAR_REGERACAO="true"
    E_PRIMEIRO_BOOT="true"
    echo ""
fi

# BLOCO 17 — Função que gera (ou mantém) uma senha dentro de um .env
preencher_se_vazio() {
    local arquivo="$1"
    local nome_var="$2"
    local comando_geracao="$3"

    local valor_atual
    valor_atual="$(grep -E "^${nome_var}=" "$arquivo" 2>/dev/null | cut -d= -f2-)"

    if [ -n "$valor_atual" ] && [ "$FORCAR_REGERACAO" != "true" ]; then
        echo -e "  ${GREEN}✓${NC} [$arquivo] $nome_var já preenchido, mantendo."
        return
    fi

    local novo_valor
    novo_valor="$(eval "$comando_geracao")"

    if grep -q "^${nome_var}=" "$arquivo"; then
        sed -i "s|^${nome_var}=.*|${nome_var}=${novo_valor}|" "$arquivo"
    else
        echo "${nome_var}=${novo_valor}" >> "$arquivo"
    fi

    echo -e "  ${GREEN}✓${NC} [$arquivo] $nome_var $([ "$FORCAR_REGERACAO" = "true" ] && echo "regerado" || echo "gerado")."
}

# BLOCO 18 — Gera/atualiza as chaves
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}        GERANDO SEGREDOS E CHAVES                         ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [ "$FORCAR_REGERACAO" = "true" ]; then
    echo -e "${YELLOW}  Modo de regeração ativado!${NC}"
    echo ""
fi

preencher_se_vazio "airflow/.env" "AIRFLOW_FERNET_KEY" \
    "python3 -c \"import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())\""
preencher_se_vazio "airflow/.env" "AIRFLOW_SECRET_KEY" \
    "python3 -c \"import secrets; print(secrets.token_hex(32))\""
preencher_se_vazio "airflow/.env" "AIRFLOW_JWT_SECRET" \
    "python3 -c \"import secrets; print(secrets.token_hex(32))\""
preencher_se_vazio "mariadb/.env" "MYSQL_ROOT_PASSWORD" \
    "python3 -c \"import secrets; print(secrets.token_urlsafe(24))\""
preencher_se_vazio "bookstack/.env" "BOOKSTACK_APP_KEY" \
    "python3 -c \"import secrets, base64; print('base64:' + base64.b64encode(secrets.token_bytes(32)).decode())\""

echo ""

# BLOCO 19 — Configura o UID do Airflow
UID_ATUAL="$(id -u)"

if grep -q '^AIRFLOW_UID=' airflow/.env; then
    sed -i "s|^AIRFLOW_UID=.*|AIRFLOW_UID=${UID_ATUAL}|" airflow/.env
else
    echo "AIRFLOW_UID=${UID_ATUAL}" >> airflow/.env
fi

AIRFLOW_UID="$UID_ATUAL"
echo -e "${GREEN}✓${NC} Usando AIRFLOW_UID=$AIRFLOW_UID"
echo ""

# BLOCO 20 — Cria o .env central na RAIZ com VALORES REAIS
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}        CRIANDO .env CENTRAL NA RAIZ                      ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Carrega todos os .env
set -a
source ./airflow/.env
source ./bookstack/.env
source ./mariadb/.env
source ./neo4j/.env
source ./fastapi/.env
source ./streamlit/.env
set +a

# Gera o .env com VALORES REAIS (sem referências circulares)
cat > .env << EOF
# ============================================
# ARQUIVO CENTRAL DE VARIÁVEIS DE AMBIENTE
# Gerado automaticamente pelo setup.sh
# NÃO EDITE MANUALMENTE - use os .env das pastas
# ============================================

# Airflow
AIRFLOW_FERNET_KEY=${AIRFLOW_FERNET_KEY}
AIRFLOW_SECRET_KEY=${AIRFLOW_SECRET_KEY}
AIRFLOW_JWT_SECRET=${AIRFLOW_JWT_SECRET}
AIRFLOW_ADMIN_USER=${AIRFLOW_ADMIN_USER}
AIRFLOW_UID=${AIRFLOW_UID}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}

# MariaDB
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
MYSQL_USER=${MYSQL_USER}
MYSQL_PASSWORD=${MYSQL_PASSWORD}
MARIADB_HOST=${MARIADB_HOST}

# Bookstack
BOOKSTACK_APP_URL=${BOOKSTACK_APP_URL}
BOOKSTACK_APP_KEY=${BOOKSTACK_APP_KEY}
BOOKSTACK_URL=${BOOKSTACK_URL}
DB_BOOKSTACK_HOST=${DB_BOOKSTACK_HOST}
DB_BOOKSTACK_USER=${DB_BOOKSTACK_USER}
DB_BOOKSTACK_PASSWORD=${DB_BOOKSTACK_PASSWORD}
DB_BOOKSTACK_DATABASE=${DB_BOOKSTACK_DATABASE}

# Neo4j
DB_NEO4J_URI=${DB_NEO4J_URI}
DB_NEO4J_USER=${DB_NEO4J_USER}
DB_NEO4J_PASSWORD=${DB_NEO4J_PASSWORD}

# FastAPI
FASTAPI_ENV=development

# Streamlit
DB_STREAMLIT_USER=${DB_STREAMLIT_USER}
DB_STREAMLIT_PASSWORD=${DB_STREAMLIT_PASSWORD}
DB_STREAMLIT_DATABASE=${DB_STREAMLIT_DATABASE}
EOF

echo -e "${GREEN}✓${NC} .env central criado com sucesso!"
echo ""

# BLOCO 21 — Ajusta permissões das pastas
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}        AJUSTANDO PERMISSÕES                              ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

mkdir -p airflow/logs airflow/dags airflow/plugins bookstack/dados bookstack/include bookstack/backups nginx/certs nginx/logs
sudo chown -R "$AIRFLOW_UID:0" airflow bookstack 2>/dev/null || true
chmod -R 775 airflow bookstack 2>/dev/null || true

echo -e "${GREEN}✓${NC} Permissões ajustadas"
echo ""

# BLOCO 22 — Validação e Aguardo do MariaDB
verificar_senha_mariadb_db() {
    # Recarrega mariadb/.env para ter a senha atualizada no shell
    if [ -f "./mariadb/.env" ]; then
        set -a
        source ./mariadb/.env
        set +a
    fi

    echo -e "${BLUE}Iniciando MariaDB para validação...${NC}"
    docker compose "${FLAGS_ENV_FILE[@]}" up -d mariadb_service

    echo -e "${YELLOW}Aguardando o MariaDB ficar totalmente pronto (pode levar até 60s)...${NC}"
    
    local tentativas=15
    local sucesso=false

    for ((i=1; i<=tentativas; i++)); do
        if docker compose "${FLAGS_ENV_FILE[@]}" exec -T mariadb_service \
            mariadb -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1;" > /dev/null 2>&1; then
            sucesso=true
            break
        fi
        sleep 5
    done

    if [ "$sucesso" = true ]; then
        echo -e "${GREEN} MariaDB pronto e senha validada com sucesso.${NC}"
        return 0
    fi

    # Se for primeiro boot e falhou, daremos mais um tempo antes de acusar erro
    if [ "$E_PRIMEIRO_BOOT" = "true" ]; then
        echo -e "${YELLOW} O MariaDB ainda está inicializando o banco do zero. Aguardando mais 20 segundos...${NC}"
        sleep 20
        if docker compose "${FLAGS_ENV_FILE[@]}" exec -T mariadb_service \
            mariadb -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1;" > /dev/null 2>&1; then
            echo -e "${GREEN} MariaDB pronto e senha validada com sucesso.${NC}"
            return 0
        fi
    fi

    echo ""
    echo -e "${RED} A senha em mariadb/.env (MYSQL_ROOT_PASSWORD) não bate com o banco já existente.${NC}"
    echo ""
    echo "O que fazer?"
    echo "  1) Cancelar para corrigir o mariadb/.env manualmente"
    echo "  2) Apagar o volume e recriar o banco do zero (PERDE os dados do BookStack)"
    echo ""
    read -rp "Digite 1 ou 2: " escolha

    case "$escolha" in
        2)
            echo "Apagando volume do MariaDB..."
            docker compose "${FLAGS_ENV_FILE[@]}" down -v
            echo " Volume removido. Recriando o banco do zero..."
            echo ""
            
            #  NOVO: Remove a flag de primeiro boot para não tentar validar novamente
            E_PRIMEIRO_BOOT="false"
            
            #  NOVO: Sobe o MariaDB novamente com o volume limpo
            echo -e "${BLUE}Recriando MariaDB com volume limpo...${NC}"
            docker compose "${FLAGS_ENV_FILE[@]}" up -d mariadb_service
            
            echo -e "${YELLOW}Aguardando o MariaDB ficar pronto (pode levar até 60s)...${NC}"
            local tentativas_recriar=15
            local sucesso_recriar=false

            for ((i=1; i<=tentativas_recriar; i++)); do
                if docker compose "${FLAGS_ENV_FILE[@]}" exec -T mariadb_service \
                    mariadb -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1;" > /dev/null 2>&1; then
                    sucesso_recriar=true
                    break
                fi
                sleep 5
            done

            if [ "$sucesso_recriar" = true ]; then
                echo -e "${GREEN} MariaDB recriado e validado com sucesso!${NC}"
                return 0
            else
                echo -e "${RED} Falha ao recriar o MariaDB. Verifique os logs.${NC}"
                echo -e "${YELLOW}   docker compose logs mariadb_service${NC}"
                exit 1
            fi
            ;;
        *)
            echo "Cancelado. Corrija o mariadb/.env e rode o script de novo."
            exit 1
            ;;
    esac
}

verificar_senha_mariadb_db
echo ""

# BLOCO 23 — Valida a montagem completa do Docker Compose
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}        VALIDANDO DOCKER COMPOSE                          ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if docker compose config > /dev/null 2>&1; then
    echo -e "${GREEN}  docker-compose.yml válido — todas as variáveis foram resolvidas.${NC}"
else
    echo -e "${RED}  ERRO: docker-compose.yml inválido ou variável faltando.${NC}"
    exit 1
fi
echo ""

# BLOCO 24 — Baixa imagens e faz o build
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}        BAIXANDO IMAGENS E BUILD                          ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo "Baixando imagens..."
tentar_com_retry "docker compose pull" docker compose pull --ignore-buildable 2>/dev/null || true

echo "Construindo imagens locais..."
tentar_com_retry "docker compose build" docker compose build 2>/dev/null || docker compose "${FLAGS_ENV_FILE[@]}" build

echo ""

# BLOCO 25 — Menu principal (com navegação)
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}        SETUP CONCLUÍDO!                                 ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Loop do menu principal
while true; do
    if menu_principal; then
        break
    else
        echo ""
        echo -e "${YELLOW}🔙 Voltando ao menu principal...${NC}"
        sleep 1
    fi
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  SETUP CONCLUÍDO COM SUCESSO!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Comandos úteis:${NC}"
echo "  docker compose ps          - Ver status dos containers"
echo "  docker compose logs -f     - Ver logs"
echo "  docker compose down        - Parar todos"
echo "  docker compose up -d       - Subir todos (usando .env da raiz)"
echo "  docker compose up -d [servico] - Subir um serviço específico"
echo ""