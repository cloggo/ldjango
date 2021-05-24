FROM python:3.9.5-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements-drf.txt ./
COPY lspider/requirements-redis.txt ./

RUN set -ex \
  && buildDeps=' \
  gcc \
  linux-libc-dev \
  libgcc-8-dev \
  python3-dev \
  ' \
  && libDeps=' \
  postgresql-client \
  libpq-dev \
  ' \
  && apt-get update && apt-get install -y $buildDeps $libDeps --no-install-recommends \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir -r requirements-redis.txt \
  && pip install --no-cache-dir -r requirements-drf.txt \
  && apt-get purge -y --auto-remove $buildDeps \
  && rm -rf /src/*

ADD . /usr/src/app/

RUN chmod +x *.sh

CMD ["./scrapy_start.sh"]
