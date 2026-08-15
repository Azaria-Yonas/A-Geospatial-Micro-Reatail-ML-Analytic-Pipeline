from psql.raw_data.locations import get_coordinates
from psql.raw_data.responses import get_response
from psql.data_parsing.cbp_naics_table import insert_variables





def to_int(x):
    try:
        return int(x)
    except:
        return None 




def parse_cbp_naics(zcta, state, r):
    def get_vals(key):
        try:
            vals = r[key][1]
            return to_int(vals[0]), to_int(vals[1])
        except Exception:
            return None, None

    def get_estab(key):
        try:
            return to_int(r[key][1][0])
        except Exception:
            return None



    estab_total, emp_total = get_vals("all")
    estab_1_4, emp_1_4 = get_vals("1_4")
    estab_5_9, emp_5_9 = get_vals("5_9")
    estab_10_19, emp_10_19 = get_vals("10_19")
    estab_20_49, emp_20_49 = get_vals("20_49")
    estab_50_99, emp_50_99 = get_vals("50_99")
    estab_100_249, emp_100_249 = get_vals("100_249")
    estab_250_499, emp_250_499 = get_vals("250_499")
    estab_500_999, emp_500_999 = get_vals("500_999")
    estab_1000_plus, emp_1000_plus = get_vals("1000_plus")
    estab_n01_bus = get_estab("N01_BUS")
    estab_n08_bus = get_estab("N08_BUS")
    return (
        zcta, state, estab_total,
        emp_total,estab_1_4, emp_1_4, 
        estab_5_9, emp_5_9, estab_10_19, 
        emp_10_19,estab_20_49, emp_20_49,
        estab_50_99,emp_50_99, estab_100_249,
        emp_100_249,estab_250_499, emp_250_499,
        estab_500_999, emp_500_999, estab_1000_plus, 
        emp_1000_plus, estab_n01_bus, estab_n08_bus,
    )




if __name__ == "__main__": 

    coordinates = get_coordinates()
    state = {coordinate[0]: coordinate[1] for coordinate in coordinates}

    response = get_response("cbp-naics").items() 

    for z, r in response: 
        insert_variables(*parse_cbp_naics(z, state.get(z), r))









