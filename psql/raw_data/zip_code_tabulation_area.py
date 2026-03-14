import psycopg
from .. import DATABASE, USERNAME, DB_KEY, CITY

def get_zcta (lbound = None, hbound = None):
    zcta= []

    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            if hbound is None and lbound is  None:
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s""",
                    (CITY,))
            elif hbound is None and lbound is not None: 
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s
                    OFFSET %s""",
                    (CITY, lbound))
            elif lbound is None and hbound is not None:
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s
                    FIRST %s ROWS ONLY""", 
                    (CITY, hbound))        
            else:
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s
                    OFFSET %s FETCH FIRST %s ROWS ONLY""",
                    (CITY, lbound, hbound - lbound if hbound and lbound is not None else 0)
                )
            for (z,) in curr: 
                zcta.append(z)  
    return zcta, CITY 
