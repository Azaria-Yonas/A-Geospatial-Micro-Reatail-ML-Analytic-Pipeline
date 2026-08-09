from .. import DATABASE, USERNAME, DB_KEY
import psycopg as pg



def insert_variables(
    zcta, state, total_population, median_household_income,
    per_capita_income, poverty_population,bachelors_degree, 
    employed_population, housing_units, median_gross_rent, 
    public_transport_users, total_commuters, aggregate_commute_time,
    no_vehicle_households,renter_occupied,owner_occupied,total_occupied, 
    food_stamp_households, total_households, owner_no_vehicle_households,
):
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO  parsed_data.acs_variables (
                    zcta, state, total_population, median_household_income,
                    per_capita_income, poverty_population,bachelors_degree, 
                    employed_population, housing_units, median_gross_rent, 
                    public_transport_users, total_commuters, aggregate_commute_time,
                    no_vehicle_households,renter_occupied,owner_occupied,total_occupied, 
                    food_stamp_households, total_households, owner_no_vehicle_households

                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                (
                    zcta, state, total_population, median_household_income,
                    per_capita_income, poverty_population,bachelors_degree, 
                    employed_population, housing_units, median_gross_rent, 
                    public_transport_users, total_commuters, aggregate_commute_time,
                    no_vehicle_households,renter_occupied,owner_occupied,total_occupied, 
                    food_stamp_households, total_households, owner_no_vehicle_households
                ))



def get_variables(state = None, lbound = None, hbound = None, *args): 
    cols = ", ".join(args) if args else "*"
    
    variables = []



    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:


            parameters = []

            query = f"SELECT {cols} FROM parsed_data.acs_variables" 



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





