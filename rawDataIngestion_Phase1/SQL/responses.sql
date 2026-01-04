CREATE TABLE responses(
    Index_num BIGSERIAL NOT NULL,
    ID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    zip INT REFERENCES zipCodes(zip),


    Places JSON,
    Overpass JSON,
    ArcGIS JSON,
    Census JSON
)