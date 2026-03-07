CREATE TABLE requests(
    index_num BIGSERIAL NOT NULL,
    status_code INT,   
    
    zcta INT REFERENCES zcta(zcta),
    api VARCHAR(8) NOT NULL CHECK (api IN ('places','overpass','arcgis','census')),
    attempt INT,


    error_message TEXT,
    endpoint VARCHAR,
    method VARCHAR(4) NOT NULL CHECK (method IN ('POST','GET')),
    headers JSONB,
    body JSONB,
     
    
    date_time TIMESTAMPTZ DEFAULT now(),
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);


CREATE INDEX requests_zcta_and_api ON requests(zcta, api);
CREATE INDEX requests_status_code ON requests(status_code);
CREATE INDEX requests_date_time ON requests(date_time);
