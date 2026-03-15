from psql.raw_data.responses import get_response
from psql.data_processing.census_table import insert_variables


def to_int(x):
    try:
        return int(x)
    except:
        return 0



def parse_census(zcta, r):
    return (
        zcta, 
        to_int(r[1][1]),   # B01003_001E
        to_int(r[1][2]),   # B19013_001E
        to_int(r[1][3]),   # B19301_001E
        to_int(r[1][4]),   # B17001_002E
        to_int(r[1][5]),   # B15003_022E
        to_int(r[1][6]),   # B23025_004E
        to_int(r[1][7]),   # B25001_001E
        to_int(r[1][8]),   # B25064_001E
        to_int(r[1][9]),   # B08301_010E
        to_int(r[1][10]),  # B08012_001E
        to_int(r[1][11]),  # B08013_001E
        to_int(r[1][12]),  # B08201_002E
        to_int(r[1][13]),  # B25003_003E
        to_int(r[1][14]),  # B25003_002E
        to_int(r[1][15]),  # B25003_001E
        to_int(r[1][16]),  # B01001_011E
        to_int(r[1][17]),  # B01001_012E
        to_int(r[1][18]),  # B01001_013E
        to_int(r[1][19]),  # B01001_014E
        to_int(r[1][20]),  # B01001_035E
        to_int(r[1][21]),  # B01001_036E
        to_int(r[1][22]),  # B01001_037E
        to_int(r[1][23])   # B01001_038E
    )




if __name__ == "__main__":
    response = get_response("census").items()

    for z, r in response:
        insert_variables(*parse_census(z, r))
