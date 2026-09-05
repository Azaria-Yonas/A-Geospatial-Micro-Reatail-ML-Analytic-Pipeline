from psql.raw_data.locations import get_coordinates
from psql.raw_data.responses import get_response
from psql.data_parsing.arcgis_table import insert_variables


def to_int(x):
    try:
        return int(x)
    except:
        return None


def to_float(x):
    try:
        return float(x)
    except:
        return None



def parse_arcgis(zcta, state, r): 
    try:  
        attr = (
            r["results"][0]
             ["value"]["FeatureSet"][0]
             ["features"][0]
             ["attributes"]
        )

        if to_int(attr["HasData"]) != 1:
            attr = {}

    except Exception:
        attr = {}

    return (
        zcta,state,to_int(attr.get("CHILD_CY")),to_int(attr.get("WORKAGE_CY")),
        to_int(attr.get("SENIOR_CY")), to_float(attr.get("CRMCYTOTC")),
        to_int(attr.get("DPOP_CY")), to_int(attr.get("DPOPWRK_CY")), 
        to_float(attr.get("DPOPDENSCY")), to_float(attr.get("MEDDI_CY")),
        to_float(attr.get("AVGDI_CY")), to_float(attr.get("X11002_A")), 
        to_float(attr.get("X14058_A")), to_float(attr.get("MEDVAL_CY")),
        to_float(attr.get("AVGVAL_CY")), to_float(attr.get("MEDNW_CY")), 
        to_float(attr.get("AVGNW_CY")), to_float(attr.get("X1001_X")) 
    )





if __name__ == "__main__": 
    coordinates = get_coordinates()
    state = {coordinate[0]: coordinate[1] for coordinate in coordinates}

    response = get_response("arcgis").items()


 
    for z, r in response: 
        insert_variables(*parse_arcgis(z, state.get(z), r))




