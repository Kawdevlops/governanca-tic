
docker compose --env-file ./bookstack/.env --env-file ./neo4j/.env --env-file ./mariadb/.env --env-file ./airflow/.env up airflow_init

docker compose --env-file ./bookstack/.env --env-file ./neo4j/.env --env-file ./mariadb/.env --env-file ./airflow/.env up -d --build