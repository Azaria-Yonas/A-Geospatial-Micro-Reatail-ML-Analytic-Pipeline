import asyncio
import aiohttp 
import json
from psql.raw_data.requests import insert_request
from psql.raw_data.responses import insert_response
from config import CENSUS




def get_url (year = None):
    if year is None:
        return "https://api.census.gov/data/2023/acs/acs5"
    return f"https://api.census.gov/data/{year}/acs/acs5"




def get_parameter(zcta):
    return {
        "get": ",".join([
            "NAME",

            "B01003_001E",   # 1. The total population 
            "B19013_001E",   # 2. The median household income 
            "B19301_001E",   # 3. The per capita income

            "B17001_002E",   # 4. The population below poverty
            "B15003_022E",   # 5. Population with Bachelor's degree 
     
            "B23025_004E",   # 6. The employed population 
            "B25001_001E",   # 7. Number of housing units
            "B25064_001E",   # 8. The median gross rent 
           
            "B08301_010E",   # 9. The number of public transport commuters
            "B08012_001E",   # 10. The number of total commuters 
            "B08013_001E",   # 11. The aggregate commute minutes 

            "B08201_002E",   # 12. The number of households with no vehicle 
            "B25003_003E",   # 13. The number of renter-occupied housing units 
            "B25003_002E",   # 14. The number of owner-occupied housing units 
            "B25003_001E",   # 15. The number of total occupied housing units

            "B22010_002E",   # 16. HHs getting Food Stamps 
            "B11001_001E",   # 17. Total households 
            "B25044_003E",   # 18. Owner-occupied households with no vehicle 
            
        ]),
        "for": f"zip code tabulation area:{zcta}",  
        "key": CENSUS 
    }



async def acs_tasks (session, zcta, semaphore): 
    async with semaphore:
        url = get_url()
        parameter = get_parameter(zcta)
        async with session.get(url, params = parameter) as resp:
            status = resp.status
            try: 
                response = await resp.json()        
                insert_request(zcta, "acs", url, "GET", body=parameter, status_code=status)  
            except aiohttp.ContentTypeError:
                response = await resp.text() 
                insert_request(zcta, "acs", url, "GET", body=parameter, status_code=status, error_message=response ) 
            return zcta, response, status, "acs"









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

# if __name__ == "__main__":
#     asyncio.run(func(coordinates))