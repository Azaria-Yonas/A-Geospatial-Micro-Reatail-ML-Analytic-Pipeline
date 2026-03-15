CREATE TABLE processed_data.overpass_zcta (

    index_num BIGSERIAL NOT NULL,
    zcta INT PRIMARY KEY REFERENCES raw_data.zcta(zcta),
    city TEXT, 

    bus_stops INTEGER,
    crosswalks INTEGER,
    footways INTEGER,
    roads_with_sidewalks INTEGER,
    human_scale_streets INTEGER

);


CREATE INDEX overpass_city_zcta ON processed_data.overpass_zcta (city, zcta);