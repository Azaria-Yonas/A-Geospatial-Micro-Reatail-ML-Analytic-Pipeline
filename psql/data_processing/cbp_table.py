from .. import DATABASE, USERNAME, DB_KEY, CITY
import psycopg as pg




def insert_variables(
    zcta, estab_total, emp_total,
    estab_1_4, emp_1_4,
    estab_5_9, emp_5_9,
    estab_10_19, emp_10_19,
    estab_20_49, emp_20_49,
    estab_50_99, emp_50_99,
    estab_100_249, emp_100_249,
    estab_250_499, emp_250_499,
    estab_500_999, emp_500_999,
    estab_1000_plus, emp_1000_plus,
    city = CITY
):

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO processed_data.cbp_variables (
                    zcta, city, estab_total, emp_total, 
                    
                    estab_1_4, emp_1_4,
                    estab_5_9, emp_5_9,
                    estab_10_19, emp_10_19,
                    estab_20_49, emp_20_49,
                    estab_50_99, emp_50_99,
                    estab_100_249, emp_100_249,
                    estab_250_499, emp_250_499,
                    estab_500_999, emp_500_999,
                    estab_1000_plus, emp_1000_plus
                )
                VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,
                    %s,%s,
                    %s,%s
                );
                """,
                (
                    zcta, city, estab_total, emp_total,

                    estab_1_4, emp_1_4,
                    estab_5_9, emp_5_9,
                    estab_10_19, emp_10_19,
                    estab_20_49, emp_20_49,
                    estab_50_99, emp_50_99,
                    estab_100_249, emp_100_249,
                    estab_250_499, emp_250_499,
                    estab_500_999, emp_500_999,
                    estab_1000_plus, emp_1000_plus,
                ),
            )




def get_variables(lbound = None, hbound = None, city = CITY, *args):
    cols = ", ".join(args)
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            if lbound is None and hbound is None:
                curr.execute("""
                    SELECT %s FROM processed_data.cbp_variables
                    WHERE city = %s;   
                """,
                (cols, city))
            elif hbound is None and lbound is not None: 
                curr.execute("""
                    SELECT %s FROM processed_data.cbp_variables
                    WHERE city = %s
                    OFFSET %s;
                """,
                (cols, city, lbound))
            elif lbound is None and hbound is not None:
                curr.execute("""
                    SELECT %s FROM processed_data.cbp_variables
                    WHERE city = %s
                    FIRST %s ROWS ONLY;
                """, 
                (cols, city, hbound))        
            else:
                curr.execute("""
                    SELECT %s FROM processed_data.cbp_variables
                    WHERE city = %s
                    OFFSET %s FETCH FIRST %s ROWS ONLY;
                """,
                (cols, city, lbound, hbound - lbound if hbound and lbound is not None else 0))
