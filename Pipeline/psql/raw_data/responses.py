import psycopg as pg
from psycopg.types.json import Json

from .. import DATABASE, USERNAME, DB_KEY 


def insert_response(zcta, state, api, response):
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO raw_data.responses (zcta, state, api, response) 
                VALUES (%s, %s, %s, %s);
            """, 
            (zcta, state, api, Json(response)))



def get_response(api, state = None, lbound=None, hbound=None):

    responses = {}

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            parameters = [api]


            query = "SELECT zcta, response FROM raw_data.responses WHERE api = %s"

            if state is not None:
                query += " AND state = %s"
                parameters.append(state)

            query += " ORDER BY zcta"

            if lbound is not None:
                query += " OFFSET %s"
                parameters.append(lbound)

            if hbound is not None:
                query += " FETCH FIRST %s ROWS ONLY"
                parameters.append(hbound)

            curr.execute(query=query, params=parameters)

            for (zcta,r) in curr:
                responses[zcta] = r

    return responses