from .. import DATABASE, USERNAME, DB_KEY, CITY
import psycopg as pg




def insert_variables(zcta, dtp, urb):
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO processed_data.arcgis_variables (zcta, city, daytime_population, urbanicity) 
                VALUES (%s, %s, %s, %s);
            """, 
            (zcta, CITY, dtp, urb))

def get_variables(lbound = None, hbound = None, *args):
    pass