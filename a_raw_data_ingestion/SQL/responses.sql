CREATE TABLE responses(
    index_num BIGSERIAL NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    zcta INT REFERENCES zcta(zcta),
    city VARCHAR(30),

    api VARCHAR(8) NOT NULL CHECK (api IN ('places','overpass','arcgis','census')),
    response JSONB,
    date_time TIMESTAMPTZ DEFAULT now()
);


CREATE INDEX responses_zcta_and_api ON responses(zcta, api);
CREATE INDEX responses_date_time ON responses(date_time);
CREATE INDEX responses_city_idx ON responses(city);