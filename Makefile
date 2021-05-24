IMAGE_TAG := cloggo/scrapy:lspider-1.0.20-3.9.5

.PHONE: clean push run build redis-start redis-stop crawl migrate

push:
	docker push $(IMAGE_TAG)

run:
	docker run $(IMAGE_TAG)

docker-crawl:
	docker-compose run spider python manage.py crawl

build:
	docker build -t $(IMAGE_TAG) -f Dockerfile .

redis-start:
	brew services start redis

redis-stop:
	brew services stop redis

crawl:
	python manage.py crawl

migrate:
	python manage.py makemigrations lspider
	python manage.py migrate

run-api:
	python manage.py runserver

clean:
	$(RM) -rf lspider/lspider/migrations/000* lspider/lspider/migrations/__pycache__ db.sqlite3
