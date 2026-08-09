CREATE SCHEMA IF NOT EXISTS parsed_data; 
CREATE TABLE parsed_data.arcgis_variables(
    index_num BIGSERIAL NOT NULL,


    zcta VARCHAR(5) PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    state VARCHAR(3),


    child_population INTEGER,
    working_population INTEGER,
    senior_population INTEGER,  
    total_crime_index DOUBLE PRECISION, 
    daytime_population INTEGER,
    daytime_workers INTEGER,
    daytime_population_density DOUBLE PRECISION, 
    median_disposable_income DOUBLE PRECISION,
    average_disposable_income DOUBLE PRECISION,
    avg_college_tuition DOUBLE PRECISION, 
    avg_value_of_stocks DOUBLE PRECISION,
    median_home_value DOUBLE PRECISION, 
    average_home_value DOUBLE PRECISION, 
    median_net_worth DOUBLE PRECISION,
    average_net_worth DOUBLE PRECISION, 
    total_consumer_spending DOUBLE PRECISION 
    

);




CREATE INDEX arcgis_state_zcta ON processed_data.arcgis_variables (state, zcta); 



