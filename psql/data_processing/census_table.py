from .. import DATABASE, USERNAME, DB_KEY, CITY
import psycopg as pg



def insert_variables(
    zcta,
    
    total_population,        
    median_household_income,
    per_capita_income,       

    poverty_population,      
    bachelors_degree,        
    employed_population,     

    housing_units,
    median_gross_rent,

    public_transport_users,
    total_commuters,       
    aggregate_commute_time,   
    no_vehicle_households,   

    renter_occupied,        
    owner_occupied,         
    total_occupied,    

    male_25_29,           
    male_30_34,          
    male_35_39,            
    male_40_44,      

    female_25_29,       
    female_30_34,         
    female_35_39,          
    female_40_44,        
    city = CITY,    
):
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO processed_data.census_variables (
                    zcta, city,
                    total_population,        
                    median_household_income,
                    per_capita_income,       

                    poverty_population,      
                    bachelors_degree,        
                    employed_population,     

                    housing_units,
                    median_gross_rent,

                    public_transport_users,
                    total_commuters,       
                    aggregate_commute_time,   
                    no_vehicle_households,   

                    renter_occupied,        
                    owner_occupied,         
                    total_occupied,    

                    male_25_29,           
                    male_30_34,          
                    male_35_39,            
                    male_40_44,      

                    female_25_29,       
                    female_30_34,         
                    female_35_39,          
                    female_40_44  
                               
                )
                VALUES (
                    %s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,
                    %s,%s,
                    %s,
                    %s
                );
                """,
                (
                    zcta,city,

                    total_population,               #1 
                    median_household_income,        #2
                    per_capita_income,              #3  

                    poverty_population,             #4  
                    bachelors_degree,               #5   
                    employed_population,            #6   

                    housing_units,                  #7
                    median_gross_rent,              #8

                    public_transport_users,         #9
                    total_commuters,                #10
                    aggregate_commute_time,         #11
                    no_vehicle_households,          #12

                    renter_occupied,                #13
                    owner_occupied,                 #14
                    total_occupied,                 #15

                    male_25_29,                     #16   
                    male_30_34,                     #17     
                    male_35_39,                     #18        
                    male_40_44,                     #19  

                    female_25_29,                   #20    
                    female_30_34,                   #21      
                    female_35_39,                   #22       
                    female_40_44                    #23
                ))
            


def get_variables(lbound = None, hbound = None, city = CITY, *args):
    cols = ", ".join(args)
    with pg.connect(f"dbname={DATABASE} user={USERNAME} password={DB_KEY}") as conn:
        with conn.cursor() as curr:
            if lbound is None and hbound is None:
                curr.execute("""
                    SELECT %s FROM processed_data.census_variables
                    WHERE city = %s;   
                """,
                (cols, city))
            elif hbound is None and lbound is not None: 
                curr.execute("""
                    SELECT %s FROM processed_data.census_variables
                    WHERE city = %s
                    OFFSET %s;
                """,
                (cols, city, lbound))
            elif lbound is None and hbound is not None:
                curr.execute("""
                    SELECT %s FROM processed_data.census_variables
                    WHERE city = %s
                    FIRST %s ROWS ONLY;
                """, 
                (cols, city, hbound))        
            else:
                curr.execute("""
                    SELECT %s FROM processed_data.census_variables
                    WHERE city = %s
                    OFFSET %s FETCH FIRST %s ROWS ONLY;
                """,
                (cols, city, lbound, hbound - lbound if hbound and lbound is not None else 0))
