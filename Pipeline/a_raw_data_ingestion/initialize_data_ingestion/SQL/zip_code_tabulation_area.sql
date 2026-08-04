CREATE TABLE raw_data.zcta(
    Index_num BIGSERIAL PRIMARY KEY,
    state VARCHAR(30),
    zcta INT NOT NULL,
    UNIQUE (zcta)
);


CREATE INDEX zcta_state_index ON raw_data.zcta (state);
