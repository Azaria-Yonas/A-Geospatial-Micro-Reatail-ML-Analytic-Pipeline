CREATE SCHEMA IF NOT EXISTS parsed_data;

CREATE TABLE parsed_data.dhc_variables ( 

    index_num BIGSERIAL NOT NULL,
    zcta VARCHAR(5) PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    state VARCHAR(3),



    total_population_2020 INTEGER,
    household_population INTEGER,
    urban_population INTEGER,
    rural_population INTEGER,
    median_male_age NUMERIC(4,1),
    median_female_age NUMERIC(4,1),
    male_population INTEGER,
    vacant_housing_units INTEGER,
    vacant_housing_for_rent INTEGER 
);
CREATE INDEX dhc_state_zcta ON parsed_data.dhc_variables (state, zcta);








