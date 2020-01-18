# fastapi-exploration

This is a project to experiment with FastAPI.

Starting the webserver is currently done by running `uvicorn src.main:app --reload`.


Python 3.7 (had issue with psycopg2 in python 3.8)

## Database
I'm using Postgres version 12.1.3 for my storage. As of writing this is the latest Postgres version.

Postgres has been chosen since a relational DB seemed appropriate for the application.
Other positive's that weighed in on the decision:
- AWS RDS (cloud-native) support
- previous experiences

