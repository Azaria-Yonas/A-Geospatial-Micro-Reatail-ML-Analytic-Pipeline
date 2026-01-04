CREATE TABLE requests(
    Index_num BIGSERIAL NOT NULL,
    ID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    zip INT REFERENCES zipCodes(zip),


    Places_request VARCHAR(250),
    Overpass_request VARCHAR(250),
    ArcGIS_request VARCHAR(250),
    Census_request VARCHAR(250),

    Places_status VARCHAR(250),
    Overpass_status VARCHAR(250),
    ArcGIS_status VARCHAR(250),
    Census_status VARCHAR(250),

    Date_called TIMESTAMPTZ DEFAULT now()


)
