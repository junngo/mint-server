cd /home/ec2-user/work
git clone https://github.com/junngo/mint-server.git

cp /home/ec2-user/work/stock_config.yaml /home/ec2-user/work/mint-server/stock_config.yaml

cd /home/ec2-user/work/mint-server
docker-compose -f docker-compose.prod.yml build
