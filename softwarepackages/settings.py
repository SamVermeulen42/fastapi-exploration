import os

# TODO: find a cleaner way
DB_URL = 'abc' if os.environ.get("DB_URL") is None else os.environ.get("DB_URL")
