import aiohttp
import asyncio
from psql.raw_data.requests import insert_request
from psql.raw_data.responses import insert_response
from config import CENSUS

  

URL = "https://api.census.gov/data/2020/dec/dhc" 
 

   
def get_parameter(zcta):
    return {
        "get": ",".join([  "P1_001N",      # 58. 2020 Total Population
                            "PCT13_001N",  # 59. 2020 Household Population 
                            "P2_002N",     # 60. 2020 Urban Population
                            "P2_003N",     # 61. 2020 Rural Population 
                            "P13_002N",    # 62. 2020 Median Male Age
                            "P13_003N",    # 63. 2020 Median Female Age 
                            "P12_002N",    # 64. 2020 Male Population 
                            "H3_003N",     # 65. 020 Vacant Housing Units   
                            "H5_002N",     # 66. 2020 Vacant Housing Units: For Rent
            ]),
        "for": f"zip code tabulation area:{zcta}",
        "key": CENSUS
    } 


async def dhc_tasks(session, zcta, semaphore): 
    async with semaphore: 
        parameter = get_parameter(zcta) 
        async with session.get(URL, params=parameter) as resp:
            status = resp.status 
            try: 
                response = await resp.json() 
                insert_request(zcta, "dhc", URL, "GET", body=parameter, status_code=status) 
            except aiohttp.ContentTypeError:
                response = await resp.text()
                insert_request(zcta, "dhc", URL, "GET", body=parameter, status_code=status, error_message=response)
            return zcta, response, status, "dhc"


 




###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################



# async def func(coordinate): 
#     async with aiohttp.ClientSession() as session:
#         tasks = [dhc_tasks(session,  coordinate[0])]
#         results = await asyncio.gather(*tasks)
#         for z ,r, s, n in results:
#             if s == 200:
#                 print(r) 
#                 insert_response(z, "test", "dch", r)  


# coordinates = ( 98103, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# if __name__ == "__main__":
#     asyncio.run(func(coordinates))