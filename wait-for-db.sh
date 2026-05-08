#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

until mysqladmin ping -h"$host" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
  echo "MySQL está indisponível - aguardando..."
  sleep 2
done

echo "MySQL está pronto! Executando migrações e iniciando o servidor..."
python manage.py migrate
exec $cmd
