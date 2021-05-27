# lspider

## Contact

* Name: Aaron Hai Kim Diep
* Email: ****
* Phone: ****


## Usage

### docker-compose (recommended)

```bash
# starting services: spiders, rest api, postgresql, redis

docker-compose up -d


# wait until the database is initialized (should take about a minute) or check the log

docker-compose logs -f spider


# run spider immediately, unless you want to wait for the cron job to start at 11am or 11pm

docker-compose run spider python manage.py crawl


# verified data by testing the api

curl -H 'Accept: application/json; indent=4' "http://127.0.0.1:8000/quotes/"
curl -H 'Accept: application/json; indent=4' "http://127.0.0.1:8000/authors/"
curl -H 'Accept: application/json; indent=4' "http://127.0.0.1:8000/tags/"

```

### docker

```bash
# run scrapy spiders cron (default)
# datastore backend is sqlite3 and no redis cache
docker run --name lspider -p 8001:8000  cloggo/scrapy:lspider-no-redis-1.0.20-3.9.5


# initialize database
docker exec -t lspider python manage.py makemigrations lspider
docker exec -t lspider python manage.py migrate

# run the spiders immediately
docker exec -t lspider python manage.py crawl

# to start the REST api server
docker exec -t lspider python manage.py runserver 0.0.0.0:8000

# verified data by testing the api

curl -H 'Accept: application/json; indent=4' "http://127.0.0.1:8001/quotes/"
curl -H 'Accept: application/json; indent=4' "http://127.0.0.1:8001/authors/"
curl -H 'Accept: application/json; indent=4' "http://127.0.0.1:8001/tags/"

```

## Legalist Demo Scrapy Spider Engine

This project aims at demonstrating technical ability to use scrapy spider to download quotes from the website [toscrape.com](http://toscrape.com) and orchestrate related services.  The following summarizes the completion of software features.

### Features

#### Scrapy Engines

##### Spiders
* source: login.py, scroll.py, viewstate.py
* Login (medium) - login by posting username, password, and csrf_token
* Scroll (medium) - download quotes from each page until there is no more next_page
* ViewState (hard) - simulate author selection, tag selection, and obtain quote from search submit

##### Pipelines
* source: pipelines.py, models.py
* Pipelines is used to post-process data scraped from scroll and viewstate spiders
* Each pipeline python class is designed to handle related group of data model
* Data integrity (no duplication) is checked before commit to the database

##### Cron
* source: cron.sh
* Running spider daily at 11am and 11pm
* The cron job is implemented entirely using bash script
* Calculated the number of second until 11am or 11pm place the loop in sleep for that duration

##### Rate limit
* source: lspider/settings_scrapy_django_redis.py
* In order to reduce loading on the toscrape.com site, download rate was set to 125ms

#### Postgresql
* source: schema.md, models.py, ldjango/settings.py, docker-compose.yml
* The database is runned in a separate container orchestrated by using docker-compose
* The scraped data is stored in postgresql relational database
* The database parameters can be set by setting environment variables, i.e., DB_HOST, DB_NAME,...
* The database model is implemented with django ORM

##### Schema

* Author: (pk, name), unique index name
* AuthorSlug: (pk, author_pk, slug)
* Tag: (pk, tag), unique index tag
* LinkType: (pk, type)
* AuthorLink: (pk, author_pk, link_type_pk, link)
* Quote: (author_pk, created_at, updated_at, quote), unique index quote
* QuoteStatus: (quote_pk, created_at, status)
* AuthorTag: (author_pk, tag_pk)
* QuoteTag: (quote_pk, tag_pk)

#### Redis
* source: lspider/settings_scrapy_django_redis.py, docker-compose.yml
* The redis cache database is runned in a separate container orchestrated by using docker-compose
* Scrapy and redis integration using rmax/scrapy-redis package
* Scrapy dupefilter came from the scrapy-redis package
* Pause/resume functionality was verified

#### Data REST API (Export JSON Data)
* source: lspider/models.py, lspider/views.py, lspider/serializers.py, ldjango/urls.py, ldjango/settings.py
* It is implemented using django rest framework
* Endpoints: /authors, /tags, /quotes
* Links representing relations from authors, tags, and quotes were included
* This API was also meant to be used as exporting data from database in JSON format

### Integration

#### Scrapy/Postgresql
* source: alive.sh, initdb.sh, ldjango/settings.py
* The spider engine service will enter infinite loop waiting for postgresql service to be ready
* The bash script detect whether the database has been initialized, and initialize if necessarily

#### Scrapy/Django
* source: management/commands/crawl.py
* a custom command for django was implemented to run the spiders

### Design Considerations

#### General
* Python packages, libraries, and tools were chosen based on the Legalist team recommendation
* It is preferable to stick with the team preference even if one was used to using other tools; unless another way of accomplish the same task could potentially add significant values
* Code was refactored to be orthogonal, reduce repetition and increases reuses

#### Non-blocking / Concurrency (Handling Pagination)
* Scrapy request is based on twisted framework which uses a non-blocking event loop to send requests
* Using simple for-loop to iterate over scrolling pagination led to wasted processing time because extra requests were sent before the loop was stopped by has_next=False condition (no more page)
* Recursion requests or setting CONCURRENT_REQUESTS=1 can avoid processing wasteful empty quote pages 
* Because the time to parse the response and the delay in receiving response from the server is finite and bounded, the number of extra empty pages is also bounded; and thus, does not grow in proportion with the increasing number of actual non-empty page

#### Logging
* Using docker logs -f and docker-compose logs -f to examine debug info

### To Do
* Unit test REST api
* There are more works to clean up and improves
* Running splash in container and integrated with the scrapy spider

### Efforts

* It took close to 18 hours to document, test, integrate, research, plan, and implement all the listed features
