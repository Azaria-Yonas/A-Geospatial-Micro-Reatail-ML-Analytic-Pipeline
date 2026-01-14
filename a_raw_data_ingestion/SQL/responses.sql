CREATE TABLE responses(
    index_num BIGSERIAL NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    zcta INT REFERENCES zcta(zcta),

    api VARCHAR(50),
    response JSONB,
    date_time TIMESTAMPTZ DEFAULT now()
);


CREATE INDEX responses_zcta_and_api ON responses(zcta, api);
CREATE INDEX responses_date_time ON responses(date_time);