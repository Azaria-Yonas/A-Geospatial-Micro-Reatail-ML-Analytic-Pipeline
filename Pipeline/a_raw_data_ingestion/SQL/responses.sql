CREATE TABLE raw_data.responses(
    index_num BIGSERIAL NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    zcta VARCHAR(5) REFERENCES raw_data.zcta(zcta),
    state VARCHAR(30),

    api VARCHAR(16) NOT NULL, 
    response JSONB,
    date_time TIMESTAMPTZ DEFAULT now()
);


CREATE INDEX responses_zcta_and_api ON raw_data.responses(zcta, api);
CREATE INDEX responses_date_time ON raw_data.responses(date_time);
CREATE INDEX responses_state_idx ON raw_data.responses(state); 