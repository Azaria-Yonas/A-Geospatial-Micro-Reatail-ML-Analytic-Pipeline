import psycopg



def get_zipcodes (name, user, key, lbound = None, ubound = None):
    zipcodes= []

    with psycopg.connect(f"dbname={name} user={user} password={key}") as conn:
        with conn.cursor() as curr:

            if ubound is None and lbound is  None:
                curr.execute("""
                    SELECT zip FROM zipCodes
                """)
            elif ubound is None and lbound is not None: 
                curr.execute(f"""
                    SELECT zip FROM zipCodes OFFSET {lbound} 
                """)
            elif lbound is None and ubound is not None:
                curr.execute(f"""
                    SELECT zip FROM zipCodes FIRST {ubound} ROWS ONLY
                """)        
            else:
                curr.execute(f"""
                    SELECT zip FROM zipCodes OFFSET {lbound} FETCH FIRST {ubound - lbound} ROWS ONLY
                """)
            for (zip,) in curr: 
                zipcodes.append(zip)  
    return zipcodes 






