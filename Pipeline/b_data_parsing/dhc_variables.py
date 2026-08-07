from psql.raw_data.locations import get_coordinates
from psql.raw_data.responses import get_response
from psql.data_parsing.dhc_table import insert_variables






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

    



def parse_dhc(zcta, state, r): 
    try: 
        vals = r[1]
    except Exception:
        vals = []

    def get_val(i, cast=to_int):
        try: 
            return cast(vals[i])
        except Exception:
            return cast(None)

    return (
        zcta, state,
        get_val(0), get_val(1),
        get_val(2), get_val(3), 
        get_val(4, to_float),
        get_val(5, to_float),
        get_val(6), get_val(7),
        get_val(8) 
    )





if __name__ == "__main__": 
    coordinates = get_coordinates()
    state = {coordinate[0]: coordinate[1] for coordinate in coordinates}

    response = get_response("dhc").items()

    for z, r in response: 
        insert_variables(*parse_dhc(z, state.get(z), r))





