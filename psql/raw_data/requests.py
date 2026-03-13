import psycopg
from psycopg.types.json import Json

from . import DATABASE, USERNAME, DB_KEY


def insert_request(zcta, api, endpoint, method, status_code, error_message = None, headers = None, body = None):
    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            curr.execute("""
                INSERT INTO raw_data.requests (zcta, api, endpoint, method, headers, body, status_code, error_message)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (zcta, api, endpoint, method, Json(headers), Json(body), status_code, error_message))  