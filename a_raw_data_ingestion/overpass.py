import asyncio
import aiohttp
import json
from psql.requests import insert_request
from psql.responses import insert_response

URL = "https://overpass-api.de/api/interpreter"

def get_query (bbox):
    return f"""
        [out:json][timeout:180];
        /* 0 ─ Transit (bus) */
        (
        node["highway"="bus_stop"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        node["public_transport"="platform"]["bus"="yes"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        node["public_transport"="stop_position"]["bus"="yes"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        node["amenity"="bus_station"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        way["amenity"="bus_station"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        relation["amenity"="bus_station"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out count;
        /* 1 ─ Crosswalks */
        (
        node["highway"="crossing"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        way["highway"="crossing"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out count;
        /* 2 ─ Footways / pedestrian paths */
        (
        way["highway"~"^(footway|pedestrian)$"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out count;
        /* 3 ─ Roads with sidewalks */
        (
        way["highway"]["sidewalk"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out count;
        /* 4 ─ Human-scale streets */
        (
        way["highway"~"^(living_street|residential|unclassified|tertiary|service)$"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out count;
    """
    



async def overpass_tasks(session, coordinates):
    query = get_query(coordinates[1])
    async with session.post(URL, data={"data": query}) as resp:
        status = resp.status
        try: 
            response = await resp.json()        
            insert_request(coordinates[0], "overpass", URL, "POST", body=query, status_code=status)
        except aiohttp.ContentTypeError:
            response = await resp.text()
            insert_request(coordinates[0], "overpass", URL, "POST", body=query, status_code=status, error_message=response ) 
        return coordinates[0], response, status


###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################


# async def func( coordinates):
#     async with aiohttp.ClientSession() as session:
#         task = [overpass_tasks(session, coordinates)]
#         results = await asyncio.gather(*task)
#         for z, r, s in results:
#             print (z) 
#             with open("output.json", "w", encoding="utf-8") as j:
#                 json.dump(r, j, ensure_ascii=False, indent=2)


# coordinates = ( 98102, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# asyncio.run(func(coordinates))