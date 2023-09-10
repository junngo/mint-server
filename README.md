# MINT-SERVER

Welcome to Mint-Server repository! The purpose of the service is to help your finance. This repository is in charge of the server.

## Command

```
docker-compose build
docker-compose up

# Connect the database
docker exec -it mint_postgres bash
psql --username mint_server_user --dbname mint
```
