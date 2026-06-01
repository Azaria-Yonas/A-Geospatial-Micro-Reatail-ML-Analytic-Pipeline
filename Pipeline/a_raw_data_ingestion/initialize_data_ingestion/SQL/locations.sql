CREATE TABLE raw_data.locations (
    index_num BIGSERIAL NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    zcta INT UNIQUE REFERENCES raw_data.zcta(zcta),
    city VARCHAR(30),
    down_lat FLOAT,
    left_long FLOAT,
    up_lat FLOAT,
    right_long FLOAT,
    center_lat DOUBLE PRECISION GENERATED ALWAYS AS ((down_lat + up_lat) / 2) STORED,
    center_long DOUBLE PRECISION GENERATED ALWAYS AS ((left_long + right_long) / 2) STORED,
    radius DOUBLE PRECISION GENERATED ALWAYS AS (
        sqrt(
            power((((down_lat + up_lat) / 2) - down_lat) * 111320, 2) +
            power(((((left_long + right_long) / 2) - left_long) * 111320 * cos(radians(((down_lat + up_lat) / 2)))), 2)
        )
    ) STORED
    
);


CREATE INDEX locations_city_index ON raw_data.locations (city);

