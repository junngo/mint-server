cd /home/ec2-user/work/mint-server

docker-compose -f docker-compose.prod.yaml build
docker-compose -f docker-compose.prod.yaml up -d
