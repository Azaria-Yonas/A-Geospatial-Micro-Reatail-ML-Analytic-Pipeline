import asyncio
import aiohttp
import os
from psql.requests import insert_request
from psql.responses import insert_response



URL = "https://geoenrich.arcgis.com/arcgis/rest/services/World/GeoEnrichmentServer/GeoEnrichment/enrich"

API_KEY = os.getenv("ArcGIS")  



import json

def get_body(zcta):
    return {
        "f": "json",
        "API_KEY": API_KEY,  
        "studyAreas": json.dumps([{
            "sourceCountry": "US",
            "layer": "US.ZIP5",
            "ids": [str(zcta)]
        }]),
        "analysisVariables": ",".join([
            "DaytimePopulation.DPOP_CY",
            "X1130_X",
            "IND7225_X"
        ]),
        "returnGeometry": "false"
    }



async def arcgis_tasks(session,zcta):
    body = get_body(zcta)
    async with session.post(URL, data=body ) as resp:
        status = resp.status
        try:
            response = await resp.json(content_type=None)        
            insert_request(zcta, "arcgis", URL, "POST", body=body, status_code=status) 
        except aiohttp.ContentTypeError:
            response = await resp.text() 
            insert_request(zcta, "arcgis", URL, "POST", body=body, status_code=status, error_message=response ) 
        return zcta, response, status





###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################


# async def func(coordinate):
#     async with aiohttp.ClientSession() as session:
#         tasks = [arcgis_tasks(session,  coordinate[0])]
#         results = await asyncio.gather(*tasks)
#         for z ,r, s in results:
#             if s == 200:
#                 insert_response(z, "arcgis", r)  


# coordinates = ( 98102, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# asyncio.run(func(coordinates))