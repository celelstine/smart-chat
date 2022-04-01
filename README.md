# smart-chat
An engaging chatting solution that drives buisnesses conversaton between companies and clients

### Important Dependencies
- docker
- docker-compose
- Django
- djangorestframework
- Postgres
- redis
- celery


## How to run (this assumes that you can run make commands else enter the command manually)
- ensure that you have docker and docker-compose running
- start the docker stack via `make up`
- catch with db changes, apply migrations `make  migrate`
- run a health check as http://localhost:8000/health/
- Run `make logs` to follow the activities of the app

## How to test (we dont like surprises right :) )
-  run `make test`

