from psql.raw_data.responses import get_response
from psql.data_processing.arcgis_table import insert_variables

def parse_arcgis(zcta, r):
    try:
        attr = (
            r["results"][0]
             ["value"]["FeatureSet"][0]
             ["features"][0]
             ["attributes"]
        )

        if int(attr["HasData"]) == 1:
            return (zcta, int(attr["DPOP_CY"]), attr["URBNAME"])
        else:
            return (zcta, 0, None)

    except Exception:
        return (zcta, 0, None)




if __name__ == "__main__":
    response = get_response("arcgis").items()

    for z, r in response:
        insert_variables(*parse_arcgis(z, r))
