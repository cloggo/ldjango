#!/bin/bash

echo "Check whether database has been initialized..."


DB_NAME=${DB_NAME:-lspider}
DB_USER=${DB_USER:-lspider}
DB_PASSWORD=${DB_PASSWORD:-lspider8898}
DB_HOST=${DB_HOST:-pq}
DB_PORT=${DB_PORT:-5432}

SQL="SELECT 1 FROM information_schema.tables WHERE table_name='lspider_author';"

ret=$(PGPASSWORD=${DB_PASSWORD} psql -U ${DB_USER} -h ${DB_HOST} -p ${DB_PORT} ${DB_NAME} -c "${SQL}" | grep "0 row")

if [ $? -eq 0 ]; then
    echo "Initializing database...."
	  python manage.py makemigrations lspider
	  python manage.py migrate
fi
