# Mint-Server

Welcome to Mint-Server repository! The purpose of the service is to help your finance. This repository is in charge of the server. If you want to see the frontend, Let's move to the [mint-frontend repository](https://github.com/junngo/mint-frontend).

## Install & Run command

```
# 프로젝트 설치 및 실행
git clone https://github.com/junngo/mint-server.git
docker-compose build
docker-compose run

# 테스트 코드
docker-compose exec web python manage.py test

# admin 계정 생성
docker-compose exec web python manage.py createsuperuser

# db 접속
docker exec -it mint_postgres bash
psql --username mint_server_user --dbname mint

# db데이터(volume) 삭제
docker-compose down --volumes
```

## Batch Job List

```
docker-compose exec web python manage.py runjob --job stock_list_kr
```