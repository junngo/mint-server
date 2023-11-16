# MINT-SERVER

Welcome to Mint-Server repository! The purpose of the service is to help your finance. This repository is in charge of the server.

## Command

```
git clone https://github.com/junngo/mint-server.git
docker-compose build
docker-compose up

# Connect the database
docker exec -it mint_postgres bash
psql --username mint_server_user --dbname mint

# Create admin ID
docker-compose exec web python manage.py createsuperuser

# Running the test
docker-compose exec web python manage.py test # when running the container
docker-compose run web python manage.py test # when not Running the container
```

## Batch Job List

```
# [KRX] Get the company info such as name, code, sector
docker-compose exec web python manage.py co_info

# [KIS] Get the token from the KIS to access the API
docker-compose exec web python manage.py create_token

# [KIS] Get the stock price from the KIS
docker-compose exec web python manage.py gather_stock_price # If there is not date param, Call the today's date
docker-compose exec web python manage.py gather_stock_price -s 20231101 -e 20231103
```
