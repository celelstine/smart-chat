
help:
	@echo "up                     Start all docker services in background"
	@echo "down                   Shut down all services"
	@echo "shell                  Start an IPython shell session"
	@echo "sh					  Start docker shell"
	@echo "test                   Run the test suite"
	@echo "logs                   Tail the logs"
	@echo "migrate				  Run database migrations"


up:
	docker-compose up -d

down:
	docker-compose down

shell:
	docker-compose exec web python manage.py shell

sh:
	docker-compose exec web bash

test: 
	docker-compose run --rm web python manage.py test ${APP}

logs:
	docker-compose logs -f

migrate: ## Run database migrations
	docker-compose exec web python manage.py migrate ${APP}