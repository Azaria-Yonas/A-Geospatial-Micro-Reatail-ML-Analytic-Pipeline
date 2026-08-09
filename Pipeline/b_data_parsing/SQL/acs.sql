CREATE SCHEMA IF NOT EXISTS parsed_data;
CREATE TABLE parsed_data.acs_variables (
    index_num BIGSERIAL NOT NULL,
    zcta VARCHAR(5) PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    state VARCHAR(3),


    total_population INTEGER,
    median_household_income INTEGER, 
    per_capita_income INTEGER, 
    poverty_population INTEGER,
    bachelors_degree INTEGER,
    employed_population INTEGER,
    housing_units INTEGER,  
    median_gross_rent INTEGER,
    public_transport_users INTEGER,
    total_commuters INTEGER,
    aggregate_commute_time INTEGER,
    no_vehicle_households INTEGER,
    renter_occupied INTEGER,
    owner_occupied INTEGER,
    total_occupied INTEGER,
    food_stamp_households INTEGER,
    total_households INTEGER,
    owner_no_vehicle_households INTEGER

);



CREATE INDEX acs_state_zcta ON processed_data.acs_variables (state, zcta); 















