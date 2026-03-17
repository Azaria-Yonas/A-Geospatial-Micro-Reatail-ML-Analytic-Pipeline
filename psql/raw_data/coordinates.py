import psycopg
from .. import DATABASE, USERNAME, DB_KEY, CITY



def get_coordinates(city = CITY, lbound=None, hbound=None):
    coordinates = []
    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            if lbound is None and hbound is None:
                curr.execute("""
                    SELECT
                        zcta,
                        ROW(down_lat, left_long, up_lat, right_long) AS bbox,
                        ROW(center_lat, center_long, radius) AS center_and_radius
                    FROM raw_data.locations
                    WHERE city = %s""",
                (city,))
            elif lbound is not None and hbound is None:
                curr.execute("""
                    SELECT
                        zcta,
                        ROW(down_lat, left_long, up_lat, right_long) AS bbox,
                        ROW(center_lat, center_long, radius) AS center_and_radius
                    FROM raw_data.locations 
                    WHERE city = %s
                    OFFSET %s""",
                    (city, lbound))
            elif lbound is None and hbound is not None:
                curr.execute("""
                    SELECT
                        zcta,
                        ROW(down_lat, left_long, up_lat, right_long) AS bbox,
                        ROW(center_lat, center_long, radius) AS center_and_radius
                    FROM raw_data.locations 
                    WHERE city = %s                   
                    FETCH FIRST %s ROWS ONLY """,
                    (city, hbound))
            else:
                curr.execute("""
                    SELECT
                        zcta,
                        ROW(down_lat, left_long, up_lat, right_long) AS bbox,
                        ROW(center_lat, center_long, radius) AS center_and_radius
                    FROM raw_data.locations
                    WHERE city = %s
                    OFFSET %s FETCH FIRST %s ROWS ONLY""", 
                (city, lbound, hbound - lbound if hbound and lbound is not None else 0))
            for coordinate in curr:
                coordinates.append(coordinate)
    return coordinates, city

