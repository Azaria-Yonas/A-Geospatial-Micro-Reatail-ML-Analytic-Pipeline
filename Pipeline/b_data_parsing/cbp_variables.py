from psql.raw_data.responses import get_response

from Pipeline.psql.data_processing.cbp_naics_table import insert_variables

def parse_cbp(zcta, r):
    def get_vals(key):
        if r[key] is None:
            return 0, 0
        vals = r[key][1]
        estab = int(vals[0])
        emp = int(vals[1])
        return estab, emp


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


    return (
        zcta,
        estab_total,
        emp_total,
        estab_1_4,
        emp_1_4,
        estab_5_9,
        emp_5_9,
        estab_10_19,
        emp_10_19,
        estab_20_49,
        emp_20_49,
        estab_50_99,
        emp_50_99,
        estab_100_249,
        emp_100_249,
        estab_250_499,
        emp_250_499,
        estab_500_999,
        emp_500_999,
        estab_1000_plus,
        emp_1000_plus,
    )







if __name__ == "__main__":
    response = get_response("cbp").items() 


    

    for z, r in response:
        insert_variables(*parse_cbp(z, r))















    