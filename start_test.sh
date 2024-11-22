#!/bin/bash
# need chmod +
sudo mkdir -p ./dump/pgadmin;
sudo chown -R 5050:5050 dump/pgadmin/
sudo docker compose up;
sudo docker stop $(sudo docker ps -a -q);
sudo docker rm $(sudo docker ps -a -q);
sudo rm -r dump/;