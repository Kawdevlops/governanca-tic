#!/bin/bash
set -e

# Cada serviço tem seu próprio .env, dentro da própria pasta.
# Esse array é a lista única de referência — se um dia entrar um novo
# serviço com segredo próprio, só precisa adicionar a linha aqui.
ARQUIVOS_ENV=(
    "airflow/.env"
    "bookstack/.env"
    "mariadb/.env"
    "neo4j/.env"
    "fastapi/.env"
)

FLAGS_ENV_FILE=()
for arquivo in "${ARQUIVOS_ENV[@]}"; do
    FLAGS_ENV_FILE+=(--env-file "$arquivo")
done

echo "Conferindo os ${#ARQUIVOS_ENV[@]} arquivos .env..."
for arquivo in "${ARQUIVOS_ENV[@]}"; do
    if [ ! -f "$arquivo" ]; then
        echo "  $arquivo não encontrado - copiando de ${arquivo}.example..."
        cp "${arquivo}.example" "$arquivo"
    fi
    set -a
    source "$arquivo"
    set +a
done

FORCAR_REGERACAO="false"
if [ "$1" = "--regerar-segredos" ]; then
    FORCAR_REGERACAO="true"
    echo "⚠️  Modo --regerar-segredos ativado: valores existentes serão sobrescritos."
fi

if ! docker volume ls --format '{{.Name}}' | grep -qE '(^|_)mariadb_data$'; then
    echo "Nenhum volume de dados encontrado — ambiente do zero. Segredos serão gerados novos."
    FORCAR_REGERACAO="true"
fi

# preencher_se_vazio agora recebe TAMBÉM o arquivo onde a variável mora,
# porque cada segredo pertence a um .env diferente.
preencher_se_vazio() {
    local arquivo="$1"
    local nome_var="$2"
    local comando_geracao="$3"
    local valor_atual
    valor_atual="$(grep -E "^${nome_var}=" "$arquivo" 2>/dev/null | cut -d= -f2-)"

    if [ -n "$valor_atual" ] && [ "$FORCAR_REGERACAO" != "true" ]; then
        echo "  [$arquivo] $nome_var já preenchido, mantendo."
        return
    fi

    local novo_valor
    novo_valor="$(eval "$comando_geracao")"
    if grep -q "^${nome_var}=" "$arquivo"; then
        sed -i "s|^${nome_var}=.*|${nome_var}=${novo_valor}|" "$arquivo"
    else
        echo "${nome_var}=${novo_valor}" >> "$arquivo"
    fi
    echo "  [$arquivo] $nome_var $([ "$FORCAR_REGERACAO" = "true" ] && echo "regerado" || echo "gerado")."
}

tentar_com_retry() {
    local descricao="$1"
    shift
    local tentativas=3
    local espera=15
    local n=1

    until "$@"; do
        if [ "$n" -ge "$tentativas" ]; then
            echo "❌ $descricao falhou após $tentativas tentativas."
            return 1
        fi
        echo "⚠️  $descricao falhou (tentativa $n/$tentativas). Esperando ${espera}s e tentando de novo..."
        sleep "$espera"
        n=$((n + 1))
    done
}

echo "Conferindo segredos..."

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

UID_ATUAL="$(id -u)"
if grep -q '^AIRFLOW_UID=' airflow/.env; then
    sed -i "s|^AIRFLOW_UID=.*|AIRFLOW_UID=${UID_ATUAL}|" airflow/.env
else
    echo "AIRFLOW_UID=${UID_ATUAL}" >> airflow/.env
fi
AIRFLOW_UID="$UID_ATUAL"

echo "Usando AIRFLOW_UID=$AIRFLOW_UID"

mkdir -p airflow/logs airflow/dags airflow/plugins bookstack/dados bookstack/include bookstack/backups nginx/certs nginx/logs

sudo chown -R "$AIRFLOW_UID:0" airflow bookstack
chmod -R 775 airflow bookstack

verificar_senha_mariadb() {
    if ! docker volume ls --format '{{.Name}}' | grep -qE '(^|_)mariadb_data$'; then
        return 0
    fi

    docker compose "${FLAGS_ENV_FILE[@]}" up -d mariadb_service
    echo "Verificando se a senha do mariadb/.env bate com o banco existente..."
    sleep 5

    if ! docker compose "${FLAGS_ENV_FILE[@]}" exec -T mariadb_service \
        mariadb -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1;" > /dev/null 2>&1; then
        echo ""
        echo " A senha em mariadb/.env (MYSQL_ROOT_PASSWORD) não bate com o banco já existente."
        echo ""
        echo "O que fazer?"
        echo "  1) Cancelar aqui e eu mesmo corrijo o mariadb/.env manualmente"
        echo "  2) Apagar o volume e recriar o banco do zero (PERDE os dados do BookStack)"
        echo ""
        read -rp "Digite 1 ou 2: " escolha

        case "$escolha" in
            2)
                echo "Apagando volume do MariaDB..."
                docker compose "${FLAGS_ENV_FILE[@]}" down
                docker volume rm governanca-tic_mariadb_data
                echo "Volume removido. Rode o script de novo pra recriar."
                exit 0
                ;;
            *)
                echo "Cancelado. Corrija o mariadb/.env e rode o script de novo."
                exit 1
                ;;
        esac
    fi
    echo " Senha confere."
}

verificar_senha_mariadb

echo "Permissões ajustadas. Baixando imagens..."
tentar_com_retry "docker compose pull" docker compose "${FLAGS_ENV_FILE[@]}" pull --ignore-buildable

echo "Construindo imagens locais..."
tentar_com_retry "docker compose build" docker compose "${FLAGS_ENV_FILE[@]}" build

echo "Imagens prontas. Subindo os containers..."
docker compose "${FLAGS_ENV_FILE[@]}" up -d
