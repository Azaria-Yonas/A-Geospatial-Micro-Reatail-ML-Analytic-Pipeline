import psycopg


def insertIntoLocations (zip,coor, dbname, username, password):
    with psycopg.connect(f" dbname={dbname} user={username} password = {password}") as conn:
        with conn.cursor() as cur:
            if coor is (None): 
                cur.execute(f"""
                    INSERT INTO locations({zip})
                    VALUES (%s)
                """,
                (zip))
            else:
                cur.execute(f"""
                    INSERT INTO locations(zip, down_lat, left_long, up_lat, right_long)
                    VALUES (%s, %s, %s, %s, %s);
                """,
                (zip, coor[0], coor[1], coor[2], coor[3]))  
             
