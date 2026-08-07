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





def get_coordinates(state = None, lbound=None, hbound=None):
    """This function retrieves the ZCTAs along with its corresponding geographical bounding box"""

    coordinates = []
    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            conditions = []
            parameters = [] 
            


            query = "SELECT zcta, state, ROW(down_lat, left_long, up_lat, right_long) AS bbox, ROW(center_lat, center_long, radius) AS center_and_radius FROM raw_data.locations "
            if state is not None:
                conditions.append("state = %s")
                parameters.append(state)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY zcta"

            if lbound is not None:
                query += " OFFSET %s"
                parameters.append(lbound)

            if hbound is not None:
                query += " FETCH FIRST %s ROWS ONLY"
                parameters.append(hbound)

            curr.execute(query=query, params=parameters)
                                        
            coordinates = curr.fetchall()
    return coordinates


















