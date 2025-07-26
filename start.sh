#!/usr/bin/env bash
NAME="liangziduidie_demo"
DJANGODIR=/home/liangziduidie_demo
USER=root
GROUP=root
NUM_WORKERS=1
DJANGO_WSGI_MODULE=liangziduidie.wsgi


echo "Starting $NAME as `whoami`"

cd $DJANGODIR

export PYTHONPATH=$DJANGODIR:$PYTHONPATH

python manage.py makemigrations && \
  python manage.py migrate && 
  python manage.py seed_data || exit 1

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind 0.0.0.0:8000 \
--log-level=debug \
--log-file=- \
--worker-class gevent \
--threads 4