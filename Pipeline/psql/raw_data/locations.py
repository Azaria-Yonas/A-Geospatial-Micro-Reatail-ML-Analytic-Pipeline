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