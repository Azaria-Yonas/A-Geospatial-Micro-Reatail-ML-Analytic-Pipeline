import psycopg
from .. import DATABASE, USERNAME, DB_KEY 


def get_zcta (state: str | None = None, lbound: int | None = None, hbound: int | None = None):
    """This fucntion build the query based on the values specified. State filters the ZCTAs 
    by state, hbound serves as a upper bound and lbound as the lower bound, which is helpful
    if only a subset of t data is needed.""" 

    zcta= []
    states = []

    conditions = [] 
    paramerters = []
    
    if state is not None:
        conditions.append("WHERE state = %s ")
        paramerters.append(state)

    conditions.append("ORDER BY zcta")
    
    if lbound is not None:
        conditions.append("OFFSET %s")
        paramerters.append(lbound)
    
    if hbound is not None: 
        conditions.append("FETCH FIRST %s ROWS ONLY")
        paramerters.append(hbound)


    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr: 
            curr.execute("SELECT zcta, state FROM raw_data.zcta " + " ".join(conditions),
                    paramerters
                )
            for (z,s) in curr: 
                zcta.append(z)  
                states.append(s)
    return zcta, states 


def load_zcta(state, zcta): 
    """This funciton is loads the raw zcta from each state into a the zcta table.""" 

    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn: 
        with conn.cursor() as curr: 
            curr.executemany("""
                INSERT INTO raw_data.zcta (state, zcta) VALUES (%s, %s)
                ON CONFLICT (zcta) DO NOTHING 
            """, 
            [(state, z) for z in zcta]) 