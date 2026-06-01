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



def get_response(api, city = CITY, lbound=None, hbound=None):

    responses = {}

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            if lbound is None and hbound is None:

                curr.execute("""
                    SELECT zcta ,response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                """, (city, api))
            elif lbound is not None and hbound is None:
                curr.execute("""
                    SELECT zcta, response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                    OFFSET %s
                """, (city, api, lbound))
            elif lbound is None and hbound is not None:
                curr.execute("""
                    SELECT zcta, response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                    FETCH FIRST %s ROWS ONLY
                """, (city, api, hbound))
            else:
                curr.execute("""
                    SELECT zcta, response
                    FROM raw_data.responses
                    WHERE city = %s AND api = %s
                    OFFSET %s
                    FETCH FIRST %s ROWS ONLY
                """, (city, api, lbound, hbound - lbound if hbound and lbound is not None else 0))
            for (zcta,r) in curr:
                responses[zcta] = r

    return responses