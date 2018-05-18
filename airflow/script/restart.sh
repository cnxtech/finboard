#!/usr/bin/env bash

echo "Restart..."

set -o errexit

# Remove docker container
if [ "$(docker ps -a | grep airflow)" ]; then
    echo "Remove docker container"
    docker rm -f airflow
fi

echo "Update git repository"
pushd /home/ec2-user/finboard/airflow
git pull

echo "Start docker container"
docker run -it -d -p 8080:8080 --name airflow \
    --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    -v /home/ec2-user/airflow:/data:ro \
    airflow:latest
popd

sleep 30
echo "Start airflow scheduler"
docker exec airflow airflow scheduler -D