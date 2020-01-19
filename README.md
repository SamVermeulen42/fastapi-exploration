# fastapi-exploration

This is a project to experiment with FastAPI.

Python 3.7 (had issue with psycopg2 in python 3.8)

## Database
I'm using Postgres version 12.1.3 for my storage. As of writing this is the latest Postgres version.

Postgres has been chosen since a relational DB seemed appropriate for the application.
Other positive's that weighed in on the decision:
- AWS RDS (cloud-native) support
- previous experiences

## docker

docker build . -t sam/fastapi:1.0
docker run -p 8000:8000 --env-file=.env sam/fastapi:1.0
