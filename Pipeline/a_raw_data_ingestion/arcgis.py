import asyncio
import aiohttp
import json
import os
from psql.raw_data.requests import insert_request
from psql.raw_data.responses import insert_response
from config import ARGIS


URL = "https://geoenrich.arcgis.com/arcgis/rest/services/World/GeoEnrichmentServer/GeoEnrichment/enrich" 




def get_body(zcta):
    return {
        "f": "json",
        "token": ARGIS,  
        "studyAreas": json.dumps([{
            "sourceCountry": "US",
            "layer": "US.ZIP5", 
            "ids": zcta 
        }]),
        "analysisVariables": ",".join([
            "AgeDependency.CHILD_CY",        # 19. 2026 Child Population 
            "AgeDependency.WORKAGE_CY",      # 20. 2026 Working Population 
            "AgeDependency.SENIOR_CY",       # 21. 2026 Senior Population
            "crime.CRMCYTOTC",               # 22. 2026 Total Crime Index           
            "DaytimePopulation.DPOP_CY",     # 23. 2026 Total Daytime Population
            "DaytimePopulation.DPOPWRK_CY",  # 24. 2026 Daytime Pop: Workers  
            "DaytimePopulation.DPOPDENSCY",  # 25. 2026 Daytime Pop Density
            "disposableincome.MEDDI_CY",     # 26. 2026 Median Disposable Income 
            "disposableincome.AVGDI_CY",     # 27. 2026 Average Disposable Income 
            "education.X11002_A",            # 28. 2026 Avg: College Tuition 
            "financial.X14058_A",            # 29. 2026 Avg: Value of Stocks
            "homevalue.MEDVAL_CY",           # 30. 2026 Median Home Value 
            "homevalue.AVGVAL_CY",           # 31. 2026 Average Home Value 
            "networth.MEDNW_CY",             # 32. 2026 Median Net Worth 
            "networth.AVGNW_CY",             # 33. 2026 Average Net Worth 
        ]),
        "returnGeometry": "false"
    }



async def arcgis_tasks(session,zcta):
    body = get_body(zcta)

    async with session.post(URL, data=body) as resp:
        status = resp.status
        try:
            response = await resp.json(content_type=None)        
            insert_request(zcta, "arcgis", URL, "POST", body=body, status_code=status) 
        except aiohttp.ContentTypeError:
            response = await resp.text() 
            insert_request(zcta, "arcgis", URL, "POST", body=body, status_code=status, error_message=response ) 
        return zcta, response, status, "arcgis"













###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################



# async def func(coordinate):
#     async with aiohttp.ClientSession() as session:
#         tasks = [arcgis_tasks(session,  coordinate[0])]
#         results = await asyncio.gather(*tasks)
#         for z ,r, s, n in results:
#             if s == 200:
#                 print(r)
#                 insert_response(z, "test", "arcgis", r)  


# coordinates = ( 98103, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# if __name__ == "__main__":
#     asyncio.run(func(coordinates))