import asyncio
import aiohttp
import json
import os
from psql.requests import insert_request
from psql.responses import insert_response



URL = "https://geoenrich.arcgis.com/arcgis/rest/services/World/GeoEnrichmentServer/GeoEnrichment/enrich"

API_KEY = os.getenv("ArcGIS")  



def get_body(zcta):
    return {
        "f": "json",
        "token": API_KEY,  
        "studyAreas": json.dumps([{
            "sourceCountry": "US",
            "layer": "US.ZIP5",
            "ids": [str(zcta)]
        }]),
        "analysisVariables": ",".join([
            "DaytimePopulation.DPOP_CY",
            "businesses.N04_BUS",   # businesses with 1–4 employees
            "businesses.N05_BUS",   # businesses with 5–9 employees
            "urbanicity.URBNAME"    # City classification
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
#                 insert_response(z, "test", "arcgis", r)  


# coordinates = ( 98103, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# asyncio.run(func(coordinates))