CREATE SCHEMA IF NOT EXISTS raw_data: 
DROP TABLE IF EXISTS raw_data.zcta; 
CREATE TABLE raw_data.zcta(
    Index_num BIGSERIAL PRIMARY KEY,
    state VARCHAR(3), 
    zcta VARCHAR(5) NOT NULL, 
    UNIQUE (zcta)
);


CREATE INDEX zcta_state_index ON raw_data.zcta (state);
