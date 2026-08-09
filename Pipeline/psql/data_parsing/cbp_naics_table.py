from .. import DATABASE, USERNAME, DB_KEY
import psycopg as pg


def insert_variables(
    zcta, state, estab_total, emp_total,
    estab_1_4, emp_1_4, estab_5_9, emp_5_9,
    estab_10_19, emp_10_19, estab_20_49, 
    emp_20_49, estab_50_99, emp_50_99,
    estab_100_249, emp_100_249, estab_250_499, 
    emp_250_499, estab_500_999, emp_500_999,
    estab_1000_plus, emp_1000_plus,
    estab_n01_bus, estab_n08_bus,
):

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO parsed_data.cbp_naics_variables (
                    zcta, state, estab_total, emp_total,
                    estab_1_4, emp_1_4, estab_5_9, emp_5_9,
                    estab_10_19, emp_10_19, estab_20_49, 
                    emp_20_49, estab_50_99, emp_50_99,
                    estab_100_249, emp_100_249, estab_250_499, 
                    emp_250_499, estab_500_999, emp_500_999,
                    estab_1000_plus, emp_1000_plus,
                    estab_n01_bus, estab_n08_bus
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                (
                    zcta, state, estab_total, emp_total,
                    estab_1_4, emp_1_4, estab_5_9, emp_5_9,
                    estab_10_19, emp_10_19, estab_20_49, 
                    emp_20_49, estab_50_99, emp_50_99,
                    estab_100_249, emp_100_249, estab_250_499, 
                    emp_250_499, estab_500_999, emp_500_999,
                    estab_1000_plus, emp_1000_plus,
                    estab_n01_bus, estab_n08_bus,
                ),
            )






def get_variables(state = None, lbound = None, hbound = None, *args): 
    cols = ", ".join(args) if args else "*"

    variables = []

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            parameters = []


            query = f"SELECT {cols} FROM parsed_data.cbp_naics_variables"

            if state is not None:
                query += " WHERE state = %s"
                parameters.append(state)

            query += " ORDER BY zcta"

            if lbound is not None:
                query += " OFFSET %s"
                parameters.append(lbound)

            if hbound is not None:
                query += " FETCH FIRST %s ROWS ONLY"
                parameters.append(hbound)

            curr.execute(query=query, params=parameters)

            variables = curr.fetchall()

    return variables
