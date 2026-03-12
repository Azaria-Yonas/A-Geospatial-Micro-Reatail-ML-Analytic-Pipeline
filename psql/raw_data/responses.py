import psycopg
from psycopg.types.json import Json

from . import RAWDATA, USERNAME, DB_KEY

def insert_response(zcta, city, api, response):
    with psycopg.connect(f"dbname={RAWDATA} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO responses (zcta, city, api, response) 
                VALUES (%s, %s, %s, %s);
            """, 
            (zcta, city, api, Json(response)))