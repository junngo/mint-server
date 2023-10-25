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
# Get the company info such as name, code, sector
docker-compose exec web python manage.py co_info
```
