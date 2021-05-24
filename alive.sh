#!/bin/bash

DB_NAME=${DB_NAME:-lspider}
DB_USER=${DB_USER:-lspider}
DB_PASSWORD=${DB_PASSWORD:-lspider8898}
DB_HOST=${DB_HOST:-pq}
DB_PORT=${DB_PORT:-5432}

ret=$(pg_isready -d ${DB_NAME} -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -q)

while [[ $? -ne 0 ]]; do
    ret=$(pg_isready -d ${DB_NAME} -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -q)
done
