import psycopg
from .. import DATABASE, USERNAME, DB_KEY


def insert_location (zcta, state, bbox): 
    """This function serves to insert the coordinate representations of each ZCTA into the table locations"""
    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as cur:
            if bbox is (None): 
                cur.execute("""
                    INSERT INTO raw_data.locations(zcta, state, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (zcta, state, 0 , 0 , 0 , 0))
            else:
                cur.execute("""
                    INSERT INTO raw_data.locations(zcta, state, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (zcta, state, bbox[0], bbox[1], bbox[2], bbox[3]))  




def get_errors():
    """This function extracts insertions of bad requests for retries."""

    results = [] 

    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn: 
        with conn.cursor() as curr: 
            curr.execute("""
                SELECT zcta, state FROM raw_data.locations WHERE down_lat = 0 OR up_lat = 0 OR left_long = 0 OR right_long = 0
            """)

            results = curr.fetchall()

    return results 




def update_zcta(zcta, state, bbox):
    """This function updates the error requests with the latest retires."""
    if bbox is None: 
        return 

    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn: 
        with conn.cursor() as curr:
            curr.execute("""
                UPDATE raw_data.locations SET down_lat = %s, left_long = %s, up_lat = %s, right_long = %s
                WHERE zcta = %s AND state = %s
                """,
                (zcta, state, bbox[0], bbox[1], bbox[2], bbox[3])) 








