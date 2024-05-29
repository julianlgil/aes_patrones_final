# aes_patrones_final
# Crear Bases de datos
cd aes_patrones_final;
docker compose up -d db;
docker compose exec db bash -c "PGPASSWORD=aes psql -h db -p 5432 -U postgres -d aes_clients -c 'CREATE DATABASE aes_data;'";
docker compose exec db bash -c "PGPASSWORD=aes psql -h db -p 5432 -U postgres -d aes_clients -c 'CREATE DATABASE aes_accounts;'";
docker compose exec db bash -c "PGPASSWORD=aes psql -h db -p 5432 -U postgres -d aes_clients -c 'CREATE DATABASE aes_transactions;'";
docker compose exec db bash -c "PGPASSWORD=aes psql -h db -p 5432 -U postgres -d aes_clients -c 'CREATE DATABASE aes_clients;'";

# Comandos para correr el proyecto:
cd aes_patrones_final;
sudo chmod 777 volumes -R;
docker compose down notifications_manager; 
docker compose up --build -d notifications_manager;
docker compose logs -f --tail 1 notifications_manager;

docker compose logs -f --tail 1

sudo chmod 777 volumes -R;
docker compose down ; 
docker compose up --build -d ;
docker compose logs -f --tail 1 ;

45257