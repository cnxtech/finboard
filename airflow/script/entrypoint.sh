#!/usr/bin/env bash

export AIRFLOW_HOME=/opt/airflow

# Start airflow webserver
echo "Initialize database..."
airflow initdb
sleep 5
airflow webserver -p 8080