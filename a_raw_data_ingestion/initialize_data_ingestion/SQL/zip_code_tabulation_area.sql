CREATE TABLE zcta(
    Index_num BIGSERIAL NOT NULL,
    city VARCHAR(30),
    zcta INT PRIMARY KEY
)


CREATE INDEX zcta_city_index ON zcta (city);
