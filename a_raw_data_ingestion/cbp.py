import asyncio
import aiohttp
from psql.raw_data.requests import insert_request
from psql.raw_data.responses import insert_response



def get_url(year=None):
    if year is None:
        return "https://api.census.gov/data/2021/cbp"
    return f"https://api.census.gov/data/{year}/cbp"

SIZES = {

    "all": "001",

    "1_4": "210",
    "5_9": "220",
    "10_19": "230",
    "20_49": "241",
    "50_99": "242",
    "100_249": "251",
    "250_499": "252",
    "500_999": "254",
    "1000_plus": "260"

}


def get_parameter(zcta, size_code):

    return {
        "get": "ESTAB,EMP",
        "for": f"zip code:{zcta}",
        "EMPSZES": size_code
    }



async def fetch_size(session, url, zcta, label, size_code):
    parameter = get_parameter(zcta, size_code)
    async with session.get(url, params=parameter) as resp:
        status = resp.status
        try:
            response = await resp.json()
        except aiohttp.ContentTypeError:
            response = await resp.text()
        return label, response, status, parameter



async def cbp_tasks(session, zcta):
    url = get_url()
    tasks = []
    for label, size_code in SIZES.items():
        tasks.append(fetch_size(session, url, zcta, label, size_code))
    results_list = await asyncio.gather(*tasks)
    results = {}
    params_used = []
    overall_status = 200

    for label, response, status, parameter in results_list:
        results[label] = response
        params_used.append(parameter)

        if status != 200:
            overall_status = status

    insert_request(zcta, "census", url, "GET", body=params_used, status_code=overall_status)  



    return zcta, results, overall_status, "cbp"







###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################



# async def func(coordinate):
#     async with aiohttp.ClientSession() as session:
#         tasks = [cbp_tasks(session, coordinate[0])]
#         result = await asyncio.gather(*tasks)
#         for z, r, s, n in result:
#             print(f"{s}->{z}:  {r}")


# coordinates = ( 98102, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# asyncio.run(func(coordinates))