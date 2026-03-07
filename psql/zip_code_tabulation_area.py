import psycopg
from . import DB_NAME, USERNAME, DB_KEY

def get_zcta (lbound = None, ubound = None):
    zcta= []

    with psycopg.connect(f"dbname={DB_NAME} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            if ubound is None and lbound is  None:
                curr.execute("""
                    SELECT zcta, city FROM zcta
                """)
            elif ubound is None and lbound is not None: 
                curr.execute(
                    "SELECT zcta, city FROM zcta OFFSET %s",
                    (lbound,))
            elif lbound is None and ubound is not None:
                curr.execute(
                    "SELECT zcta, city FROM zcta FIRST %s ROWS ONLY", 
                    (ubound,))        
            else:
                curr.execute(
                    "SELECT zcta, city FROM zcta OFFSET %s FETCH FIRST %s ROWS ONLY",
                    (lbound, ubound - lbound if ubound and lbound is not None else 0)
                )
            for (z,) in curr: 
                zcta.append(z)  
    return zcta 
