import psycopg as pg



def get_coordinates(dbname, username, Password, lbound=None, hbound=None):
    coordinates = []
    with pg.connect(f"dbname={dbname} user={username} password={Password}") as conn:
        with conn.cursor() as curr:
            if lbound is None and hbound is None:
                curr.execute(f"""
                    SELECT (zip, (down_lat, left_long, up_lat, right_long), ((center_lat, center_long), radius)) FROM locations
                """)
            elif lbound is not None and hbound is None:
                curr.execute(f"""
                    SELECT (zip, (down_lat, left_long, up_lat, right_long), ((center_lat, center_long), radius)) FROM locations
                    OFFSET {lbound}
                """)
            elif lbound is None and hbound is not None:
                curr.execute(f"""
                    SELECT (zip, (down_lat, left_long, up_lat, right_long), ((center_lat, center_long), radius)) FROM locations
                    FETCH FIRST {hbound}
                """)
            else:
                curr.execute(f"""
                    SELECT (zip, (down_lat, left_long, up_lat, right_long), ((center_lat, center_long), radius)) FROM locations
                    OFFEST {lbound} FETCH FRIST {hbound} ROWS ONLY    
                """)
            for (coor,) in curr:
                coordinates.append(coor)
    return coordinates




# This functions simply fetches the coordinates from the locations table 
# The coordiantes will be used specify the area of interest to the APIs