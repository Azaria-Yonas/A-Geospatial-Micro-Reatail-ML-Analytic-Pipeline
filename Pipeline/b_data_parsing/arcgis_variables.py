from psql.raw_data.responses import get_response
from psql.data_parsing.arcgis_table import insert_variables


def to_int(x):
    try:
        return int(x)
    except:
        return 0


def to_float(x):
    try:
        return float(x)
    except:
        return 0.0



def parse_arcgis(zcta, state, r): 
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
    coordinates = get_coordinates()
    state = {coordinate[0]: coordinate[1] for coordinate in coordinates}

    response = get_response("arcgis").items()


 
    for z, r in response: 
        insert_variables(*parse_arcgis(z, r))
