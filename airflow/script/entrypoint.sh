#!/usr/bin/env bash

: "${AIRFLOW__CORE__FERNET_KEY:=${FERNET_KEY:=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")}}"

export AIRFLOW_HOME=/opt/airflow

# Start airflow webserver
echo "Initialize database..."
airflow initdb
sleep 5
airflow webserver -p 8080