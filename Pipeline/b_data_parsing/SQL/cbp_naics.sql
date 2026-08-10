CREATE SCHEMA IF NOT EXISTS parsed_data;

 
CREATE TABLE parsed_data.cbp_naics_variables ( 

    index_num BIGSERIAL NOT NULL,
    zcta VARCHAR(5) PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    state VARCHAR(3),


    estab_total INTEGER,  
    emp_total INTEGER,
    estab_1_4 INTEGER,
    emp_1_4 INTEGER,
    estab_5_9 INTEGER, 
    emp_5_9 INTEGER,
    estab_10_19 INTEGER,
    emp_10_19 INTEGER,
    estab_20_49 INTEGER, 
    emp_20_49 INTEGER,
    estab_50_99 INTEGER,
    emp_50_99 INTEGER,
    estab_100_249 INTEGER, 
    emp_100_249 INTEGER,
    estab_250_499 INTEGER,
    emp_250_499 INTEGER,
    estab_500_999 INTEGER,
    emp_500_999 INTEGER,
    estab_1000_plus INTEGER, 
    emp_1000_plus INTEGER,
    estab_n01_bus INTEGER,
    estab_n08_bus INTEGER 

);




CREATE INDEX cbp_naics_state_zcta ON parsed_data.cbp_naics_variables (state, zcta);








