from .. import DATABASE, USERNAME, DB_KEY
import psycopg as pg




def insert_variables(
    zcta, state, child_population,
    working_population, senior_population,
    total_crime_index, daytime_population,
    daytime_workers, daytime_population_density,
    median_disposable_income,average_disposable_income,
    avg_college_tuition, avg_value_of_stocks,
    median_home_value, average_home_value,
    median_net_worth, average_net_worth,
    total_consumer_spending,
):
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO processed_data.arcgis_variables (
                    zcta, state, child_population,
                    working_population, senior_population,
                    total_crime_index, daytime_population,
                    daytime_workers, daytime_population_density,
                    median_disposable_income,average_disposable_income,
                    avg_college_tuition, avg_value_of_stocks,
                    median_home_value, average_home_value,
                    median_net_worth, average_net_worth,
                    total_consumer_spending
                )
                VALUES (%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
            (
                zcta, state, child_population,
                working_population, senior_population,
                total_crime_index, daytime_population,
                daytime_workers, daytime_population_density,
                median_disposable_income,average_disposable_income,
                avg_college_tuition, avg_value_of_stocks,
                median_home_value, average_home_value,
                median_net_worth, average_net_worth,
                total_consumer_spending
            ))



def get_variables(state = None, lbound = None, hbound = None, *args): 
    cols = ", ".join(args) if args else "*"

    variables = []

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            parameters = []


            query = f"SELECT {cols} FROM processed_data.arcgis_variables"

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






