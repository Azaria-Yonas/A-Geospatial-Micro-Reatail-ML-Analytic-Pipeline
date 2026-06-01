import psycopg
from .. import DATABASE, USERNAME, DB_KEY


def insert_location (zcta, city, bbox):
    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as cur:
            if bbox is (None): 
                cur.execute("""
                    INSERT INTO raw_data.locations(zcta, city, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (zcta, city, 0 , 0 , 0 , 0))
            else:
                cur.execute("""
                    INSERT INTO raw_data.locations(zcta, city, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (zcta, city, bbox[0], bbox[1], bbox[2], bbox[3]))  