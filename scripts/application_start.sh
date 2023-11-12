cp /home/ec2-user/work/stock_config.yaml /home/ec2-user/work/mint-server/stock_config.yaml
cd /home/ec2-user/work/mint-server

docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
