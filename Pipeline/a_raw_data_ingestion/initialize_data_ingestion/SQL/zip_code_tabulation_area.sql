CREATE TABLE raw_data.zcta(
    Index_num BIGSERIAL NOT NULL,
    state VARCHAR(30),
    zcta INT PRIMARY KEY
);


CREATE INDEX zcta_state_index ON raw_data.zcta (state);
