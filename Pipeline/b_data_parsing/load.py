# from psql.raw_data.locations import get_coordinates
# from psql.raw_data.responses import get_response
# from b_data_parsing.acs_variables import parse_acs
# from b_data_parsing.arcgis_variables import parse_arcgis
# from b_data_parsing.cbp_naics_variables import parse_cbp_naics
# from b_data_parsing.dhc_variables import parse_dhc
# from psql.data_parsing.acs_table import insert_variables as insert_acs
# from psql.data_parsing.arcgis_table import insert_variables as insert_arcgis
# from psql.data_parsing.cbp_naics_table import insert_variables as insert_cbp_naics
# from psql.data_parsing.dhc_table import insert_variables as insert_dhc




# coordinates = get_coordinates()
# state = {coordinate[0]: coordinate[1] for coordinate in coordinates}



# API = {
#     "acs": (parse_acs, insert_acs),
#     "arcgis": (parse_arcgis, insert_arcgis),
#     "cbp-naics": (parse_cbp_naics, insert_cbp_naics),
#     "dhc": (parse_dhc, insert_dhc),
# }



# def load_data():
#     for api, (parse, insert) in API.items():
#         for z, r in get_response(api).items():
#             insert(*parse(z, state.get(z), r))







# if __name__ == "__main__":  
#     load_data()





