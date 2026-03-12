import psycopg
from . import RAWDATA, USERNAME, DB_KEY


def insert_location (zcta, city, bbox):
    with psycopg.connect(f"dbname={RAWDATA} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as cur:
            if bbox is (None): 
                cur.execute("""
                    INSERT INTO locations(zcta, city, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (zcta, city, 0 , 0 , 0 , 0))
            else:
                cur.execute("""
                    INSERT INTO locations(zcta, city, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (zcta, city, bbox[0], bbox[1], bbox[2], bbox[3]))  