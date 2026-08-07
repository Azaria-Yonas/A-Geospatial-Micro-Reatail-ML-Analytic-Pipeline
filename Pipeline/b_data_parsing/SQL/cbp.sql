CREATE TABLE processed_data.cbp_variables (
    index_num BIGSERIAL NOT NULL,

    zcta INT PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    city VARCHAR(50),   


    -- The total number of businesses
    estab_total INTEGER,   -- EMPSZES = 001 , ESTAB
    emp_total INTEGER,     -- EMPSZES = 001 , EMP


    -- The number of businesses with 1–4 employees
    estab_1_4 INTEGER,     -- EMPSZES Code = 210
    emp_1_4 INTEGER,


    -- The number of businesses with 5–9 employees
    estab_5_9 INTEGER,     -- EMPSZES Code = 220
    emp_5_9 INTEGER,


    -- The number of businesses with 10–19 employees
    estab_10_19 INTEGER,   -- EMPSZES Code = 230
    emp_10_19 INTEGER,


    -- The number of businesses with 20–49 employees
    estab_20_49 INTEGER,   -- EMPSZES Code = 241
    emp_20_49 INTEGER,


    -- The number of businesses with 50–99 employees
    estab_50_99 INTEGER,   -- EMPSZES Code = 242
    emp_50_99 INTEGER,


    -- The number of businesses with 100–249 employees
    estab_100_249 INTEGER, -- EMPSZES Code = 251
    emp_100_249 INTEGER,


    -- The number of businesses with 250–499 employees
    estab_250_499 INTEGER, -- EMPSZES Code = 252
    emp_250_499 INTEGER,


    -- The number of businesses with 500–999 employees
    estab_500_999 INTEGER, -- EMPSZES Code = 254
    emp_500_999 INTEGER,


    -- The number of businesses with 1000+ employees
    estab_1000_plus INTEGER, -- EMPSZES Code = 260
    emp_1000_plus INTEGER

);


CREATE INDEX cbp_city_zcta ON processed_data.cbp_variables (city, zcta);