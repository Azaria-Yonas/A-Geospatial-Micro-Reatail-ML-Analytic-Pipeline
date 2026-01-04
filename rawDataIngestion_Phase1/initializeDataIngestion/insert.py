import psycopg


def insertIntoLocations (zcta,bbox, dbname, username, password):
    with psycopg.connect(f" dbname={dbname} user={username} password = {password}") as conn:
        with conn.cursor() as cur:
            if bbox is (None): 
                cur.execute(f"""
                    INSERT INTO locations(zcta, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s);
                """,
                (zcta, 0 , 0 , 0 , 0))
            else:
                cur.execute(f"""
                    INSERT INTO locations(zcta, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s);
                """,
                (zcta, bbox[0], bbox[1], bbox[2], bbox[3]))  
             
