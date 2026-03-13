import asyncio
import aiohttp
import json
from psql.raw_data.requests import insert_request
from psql.raw_data.responses import insert_response




def get_url (year = None):
    if year is None:
        return "https://api.census.gov/data/2023/acs/acs5"
    return f"https://api.census.gov/data/{year}/acs/acs5"




def get_parameter(zcta):
    return {
        "get": ",".join([
            "NAME",

            "B01003_001E",   # The total population
            "B19013_001E",   # The median household income
            "B19301_001E",   # The per capita income

            "B17001_002E",   # The population below poverty
            "B15003_022E",   # Population with Bachelor's degree

            "B23025_004E",   # The employed population
            "B25001_001E",   # Number of housing units
            "B25064_001E",   # The median gross rent

            "B08301_010E",   # The number of public transport commuters
            "B08012_001E",   # The number of total commuters
            "B08013_001E",   # The aggregate commute minutes

            "B08201_002E",   # The number of households with no vehicle 
            "B25003_003E",   # The number of renter-occupied housing units
            "B25003_002E",   # The number of owner-occupied housing units
            "B25003_001E",   # The number of total occupied housing units

            "B01001_011E",   # The number of males 25–29
            "B01001_012E",   # The number of males 30–34
            "B01001_013E",   # The number of males 35–39
            "B01001_014E",   # The number of males 40–44
            "B01001_035E",   # The number of females 25–29
            "B01001_036E",   # The number of females 30–34
            "B01001_037E",   # The number of females 35–39
            "B01001_038E"    # The number of females 40–44
        ]), 
        "for": f"zip code tabulation area:{zcta}"
    }



async def census_tasks (session, zcta):
    url = get_url()
    parameter = get_parameter(zcta)
    async with session.get(url, params = parameter) as resp:
        status = resp.status
        try: 
            response = await resp.json()        
            insert_request(zcta, "census", url, "GET", body=parameter, status_code=status)  
        except aiohttp.ContentTypeError:
            response = await resp.text() 
            insert_request(zcta, "census", url, "GET", body=parameter, status_code=status, error_message=response ) 
        return zcta, response, status, "census"









###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################


# async def func(coordinate):
#     async with aiohttp.ClientSession() as session:
#         tasks = [census_tasks(session, coordinate[0])]
#         result = await asyncio.gather(*tasks)
#         for z, r, s, n in result:
#             print(f"{s}->{z}:  {r}")


# coordinates = ( 98102, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# asyncio.run(func(coordinates))