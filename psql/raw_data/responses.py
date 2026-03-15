import psycopg as pg
from psycopg.types.json import Json

from .. import DATABASE, USERNAME, DB_KEY, CITY

def insert_response(zcta, city, api, response):
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO raw_data.responses (zcta, city, api, response) 
                VALUES (%s, %s, %s, %s);
            """, 
            (zcta, city, api, Json(response)))



def get_response(api, lbound=None, hbound=None):

    responses = []

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            if lbound is None and hbound is None:

                curr.execute("""
                    SELECT response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                """, (CITY, api))
            elif lbound is not None and hbound is None:
                curr.execute("""
                    SELECT response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                    OFFSET %s
                """, (CITY, api, lbound))
            elif lbound is None and hbound is not None:
                curr.execute("""
                    SELECT response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                    FETCH FIRST %s ROWS ONLY
                """, (CITY, api, hbound))
            else:
                curr.execute("""
                    SELECT response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                    OFFSET %s
                    FETCH FIRST %s ROWS ONLY
                """, (CITY, api, lbound, hbound - lbound if hbound and lbound is not None else 0))
            for (r,) in curr:
                responses.append(r)

    return responses