
from .. import DATABASE, USERNAME, DB_KEY
import psycopg as pg


def insert_variables(
    zcta, state, total_population_2020,
    household_population, urban_population,
    rural_population, median_male_age,
    median_female_age, male_population,
    vacant_housing_units, vacant_housing_for_rent,
):


    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO parsed_data.dhc_variables (
                    zcta, state, total_population_2020,
                    household_population, urban_population,
                    rural_population, median_male_age,
                    median_female_age, male_population,
                    vacant_housing_units, vacant_housing_for_rent
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,(
                    zcta, state, total_population_2020,
                    household_population, urban_population,
                    rural_population, median_male_age,
                    median_female_age, male_population,
                    vacant_housing_units, vacant_housing_for_rent
                ),
            )




def get_variables(state = None, lbound = None, hbound = None, *args):
    cols = ", ".join(args) if args else "*"

    variables = []

    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:

            parameters = []
            query = f"SELECT {cols} FROM parsed_data.dhc_variables"


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






