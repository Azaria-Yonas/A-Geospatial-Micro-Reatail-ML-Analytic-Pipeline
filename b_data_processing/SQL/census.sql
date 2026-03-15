CREATE TABLE processed_data.census_variables (
    index_num BIGSERIAL NOT NULL,
    zcta INT PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    city VARCHAR(50), 


    total_population INTEGER,        -- B01003_001E
    median_household_income INTEGER, -- B19013_001E
    per_capita_income INTEGER,       -- B19301_001E

    poverty_population INTEGER,      -- B17001_002E
    bachelors_degree INTEGER,        -- B15003_022E
    employed_population INTEGER,     -- B23025_004E

    housing_units INTEGER,           -- B25001_001E
    median_gross_rent INTEGER,       -- B25064_001E

    public_transport_users INTEGER,  -- B08301_010E
    total_commuters INTEGER,         -- B08012_001E
    aggregate_commute_time BIGINT,   -- B08013_001E
    no_vehicle_households INTEGER,   -- B08201_002E

    renter_occupied INTEGER,         -- B25003_003E
    owner_occupied INTEGER,          -- B25003_002E
    total_occupied INTEGER,          -- B25003_001E

    male_25_29 INTEGER,              -- B01001_011E
    male_30_34 INTEGER,              -- B01001_012E
    male_35_39 INTEGER,              -- B01001_013E
    male_40_44 INTEGER,              -- B01001_014E

    female_25_29 INTEGER,            -- B01001_035E
    female_30_34 INTEGER,            -- B01001_036E
    female_35_39 INTEGER,            -- B01001_037E
    female_40_44 INTEGER             -- B01001_038E

);

CREATE INDEX census_city_zcta ON processed_data.census_variables (city, zcta);