CREATE TABLE raw_data.zcta(
    Index_num BIGSERIAL NOT NULL,
    city VARCHAR(30),
    zcta INT PRIMARY KEY
);


CREATE INDEX zcta_city_index ON raw_data.zcta (city);
