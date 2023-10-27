cd /home/ec2-user/work
git clone https://github.com/junngo/mint-server.git

cd /home/ec2-user/work/mint-server
docker-compose -f docker-compose.prod.yml build
