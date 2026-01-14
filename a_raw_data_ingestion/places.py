import asyncio
import aiohttp
import os
from psql.requests import insert_request
from psql.responses import insert_response


API_KEY = os.getenv("Places_Aggregate")


URL = "https://areainsights.googleapis.com/v1:computeInsights" 


def get_header (key):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
    }
    return headers


def get_body(coor):
    lat, long, radius = coor
    radius = int(round(radius))
    body = {
        "insights": ["INSIGHT_COUNT"],
        "filter": {
            "locationFilter": {
                "circle": {
                    "radius": 1409,
                    "latLng": {
                        "latitude": lat,
                        "longitude": long,
                        },
                    },
                },
                "typeFilter": {
                    "includedTypes": [
                        "barber_shop",
                        "nail_salon",
                        "tailor",
                        "bagel_shop",
                        "donut_shop",
                        "ice_cream_shop",
                        "juice_shop",
                        "tea_house",
                        "candy_store",
                        "butcher_shop",
                        "asian_grocery_store", 
                    ]
                },
            "operatingStatus": [
                "OPERATING_STATUS_OPERATIONAL",
            ],
            "priceLevels": [
                "PRICE_LEVEL_MODERATE",
                "PRICE_LEVEL_INEXPENSIVE"
            ],
        },
    }
    return body





async def places_tasks(session, coordinate):
    body = get_body(coordinate[2])
    async with session.post(url=URL, headers=get_header("API_KEY"), json=body) as resp:
        status = resp.status
        try: 
            response = await resp.json()        
            insert_request(coordinate[0], "places", URL, "POST", headers=get_header("API_KEY"), body=body, status_code=status) 
        except aiohttp.ContentTypeError:
            response = await resp.text() 
            insert_request(coordinate[0], "places", URL, "POST", headers=get_header("API_KEY"), body=body, status_code=status, error_message=response ) 
        return coordinate[0], response, status





###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################


# async def func(coordinate):
#     async with aiohttp.ClientSession() as session:
#         tasks = [places_tasks(session,  coordinate)]
#         results = await asyncio.gather(*tasks)
#         for z ,r, s in results:
#             if s == 200:
#                 insert_response(z, "places", r)  

            
# coordinates = ( 98102, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# asyncio.run(func(coordinates))





