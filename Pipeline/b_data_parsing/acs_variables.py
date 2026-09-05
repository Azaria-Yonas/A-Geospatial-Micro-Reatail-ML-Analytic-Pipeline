from psql.raw_data.locations import get_coordinates
from psql.raw_data.responses import get_response
from psql.data_parsing.acs_table import insert_variables








def to_int(x): 

    try:
        return int(x)
    except:
        return None




def parse_acs(zcta, state, r): 
    try:
        vals = r[1]
    except Exception:
        vals = []

    def get_val(i): 
        try: 
            return to_int(vals[i])  
        except Exception:
            return  None

    return (
        zcta,state, 
        get_val(1), get_val(2), 
        get_val(3), get_val(4),
        get_val(5),get_val(6),
        get_val(7), get_val(8), 
        get_val(9),get_val(10),
        get_val(11), get_val(12),  
        get_val(13), get_val(14),
        get_val(15),get_val(16), 
        get_val(17),get_val(18)
    )




if __name__ == "__main__": 

    coordinates = get_coordinates()
    state = {coordinate[0]: coordinate[1] for coordinate in coordinates}

    response = get_response("acs").items()

    for z, r in response: 
        insert_variables(*parse_acs(z, state.get(z), r))








