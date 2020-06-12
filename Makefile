.PHONY: rabbitmq postgres install run

rabbitmq:
	docker start poker-rabbitmq || docker run -d -p 5672:5672 -e RABBITMQ_PASSWORD=password --name poker-rabbitmq bitnami/rabbitmq

postgres:
	docker start poker-postgres || docker run -d -p 5434:5432 -e POSTGRES_DB=poker -e POSTGRES_PASSWORD=password --name poker-postgres postgres:11.7

idb:
	dropdb --if-exists poker
	createdb poker
	flask db upgrade

install:
	poetry install

run: 
	poetry run python backend.py