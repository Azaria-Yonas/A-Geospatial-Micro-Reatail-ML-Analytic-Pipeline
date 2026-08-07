import asyncio
import aiohttp
from psql.raw_data.requests import insert_request
from psql.raw_data.responses import insert_response
from config import CENSUS



def get_url(year=None):
    if year is None: 
        return "https://api.census.gov/data/2021/cbp" 
    return f"https://api.census.gov/data/{year}/cbp"


SIZES = {

    "all": "001",           # 34-35
    "1_4": "210",           # 36-37     
    "5_9": "220",           # 38-39
    "10_19": "230",         # 40-41
    "20_49": "241",         # 42-43
    "50_99": "242",         # 44-45
    "100_249": "251",       # 46-47
    "250_499": "252",       # 48-49 
    "500_999": "254",       # 50-51
    "1000_plus": "260"      # 52-53

}


def get_cbp_parameter(zcta, size_code): 

    return {
        "get": "ESTAB,"                 # 34
                "EMP",                  # 35 
        "for": f"zip code:{zcta}",
        "EMPSZES": size_code,
        "key": CENSUS
    } 



NAICS_SECTORS = { 
    "N01_BUS": "00",     # 54-55
    "N08_BUS": "44-45",  # 56-57 
}


def get_naics_parameter(zcta, naics_code):
    return {
        "get": "ESTAB",
        "for": f"zip code:{zcta}",
        "NAICS2017": naics_code,
        "key": CENSUS
    }



async def fetch_size(session, url, zcta, label, size_code, semaphore): 
    async with semaphore: 
        parameter = get_cbp_parameter(zcta, size_code) 
        async with session.get(url, params=parameter) as resp: 
            status = resp.status
            
            try:
                response = await resp.json() 
            except aiohttp.ContentTypeError: 
                response = await resp.text()
            return label, response, status, parameter



async def fetch_naics(session, url, zcta, label, naics_code, semaphore): 
    async with semaphore: 
        parameter = get_naics_parameter(zcta, naics_code) 
        async with session.get(url, params=parameter) as resp: 
            status = resp.status
            try: 
                response = await resp.json()
            except aiohttp.ContentTypeError:
                response = await resp.text() 
            return label, response, status, parameter 



async def cbp_naics_tasks(session, zcta, semaphore):
    url = get_url()
    tasks = []
    for label, size_code in SIZES.items():
        tasks.append(fetch_size(session, url, zcta, label, size_code, semaphore)) 
    for label, naics_code in NAICS_SECTORS.items():
        tasks.append(fetch_naics(session, url, zcta, label, naics_code, semaphore)) 
    results_list = await asyncio.gather(*tasks, return_exceptions=True) 
    results = {}
    params_used = []
    overall_status = 200

    for item in results_list:
        if isinstance(item, BaseException):
            overall_status = 999 
            continue

        label, response, status, parameter = item
        results[label] = response
        params_used.append(parameter)

        if status != 200:
            overall_status = status

    insert_request(zcta, "cbp", url, "GET", body=params_used, status_code=overall_status)  
    return zcta, results, overall_status, "cbp-naics" 







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

# if __name__ == "__main__":
#     asyncio.run(func(coordinates))