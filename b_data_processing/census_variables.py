from psql.raw_data.responses import get_response


def parse_census(r):
    return (
        r[1][24],   # zcta
        int(r[1][1]),   # B01003_001E
        int(r[1][2]),   # B19013_001E
        int(r[1][3]),   # B19301_001E
        int(r[1][4]),   # B17001_002E
        int(r[1][5]),   # B15003_022E
        int(r[1][6]),   # B23025_004E
        int(r[1][7]),   # B25001_001E
        int(r[1][8]),   # B25064_001E
        int(r[1][9]),   # B08301_010E
        int(r[1][10]),  # B08012_001E
        int(r[1][11]),  # B08013_001E
        int(r[1][12]),  # B08201_002E
        int(r[1][13]),  # B25003_003E
        int(r[1][14]),  # B25003_002E
        int(r[1][15]),  # B25003_001E
        int(r[1][16]),  # B01001_011E
        int(r[1][17]),  # B01001_012E
        int(r[1][18]),  # B01001_013E
        int(r[1][19]),  # B01001_014E
        int(r[1][20]),  # B01001_035E
        int(r[1][21]),  # B01001_036E
        int(r[1][22]),  # B01001_037E
        int(r[1][23])   # B01001_038E
    )


if __name__ == "__main__":
    response = get_response("census", lbound=0, hbound=2)

    i = 1
    print(response)
    for r in response:
        print(f"Result {i}: {parse_census(r)}")
        i += 1
