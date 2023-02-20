# Mint-Server

Welcome to Mint-Server repository! The purpose of the service is to help your finance. This repository is in charge of the server. If you want to see the frontend, Let's move to the [mint-frontend repository](https://github.com/junngo/mint-frontend).

## Install & Run

```
# 프로젝트 설치 및 실행
git clone https://github.com/junngo/mint-server.git
docker-compose build
docker-compose run

# db 접속
docker exec -it postgres bash
psql --username mint_server_user --dbname mint
```
