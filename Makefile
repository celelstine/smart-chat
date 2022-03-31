
help:
	@echo "up                     Start all docker services in background"
	@echo "down                   Shut down all services"
	@echo "shell                  Start an IPython shell session"
	@echo "sh					  start docker shell"
	@echo "test                   Run the test suite"
	@echo "logs                   Tail the logs"


up:
	docker-compose up -d

down:
	docker-compose down

shell:
	docker-compose exec web python manage.py shell

sh:
	docker-compose exec web bash

test: 
	docker-compose run --rm web python manage.py test ${CASE}

logs:
	docker-compose logs -f