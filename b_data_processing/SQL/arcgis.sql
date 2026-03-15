CREATE TABLE processed_data.arcgis_variables(
    index_num BIGSERIAL NOT NULL,

    zcta INT PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    city VARCHAR(50),   

    daytime_population INTEGER,

    urbanicity VARCHAR(50)

);