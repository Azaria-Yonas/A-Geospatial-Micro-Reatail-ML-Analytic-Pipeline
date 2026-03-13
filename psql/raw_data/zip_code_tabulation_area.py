import psycopg
from .. import DATABASE, USERNAME, DB_KEY, CITY

def get_zcta (lbound = None, ubound = None):
    zcta= []

    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            if ubound is None and lbound is  None:
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s""",
                    (CITY,))
            elif ubound is None and lbound is not None: 
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s
                    OFFSET %s""",
                    (CITY, lbound))
            elif lbound is None and ubound is not None:
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s
                    FIRST %s ROWS ONLY""", 
                    (CITY, ubound))        
            else:
                curr.execute("""
                    SELECT zcta FROM raw_data.zcta
                    WHERE city = %s
                    OFFSET %s FETCH FIRST %s ROWS ONLY""",
                    (CITY, lbound, ubound - lbound if ubound and lbound is not None else 0)
                )
            for (z,) in curr: 
                zcta.append(z)  
    return zcta, CITY 
