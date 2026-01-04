import os
import asyncio
import aiohttp


from zcta import get_zcta
from boundingBox import find_bbox
from insert import insertIntoLocations

DB_KEY = os.getenv("dbKey")
USER = os.getenv("psqlUser")
url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/PUMA_TAD_TAZ_UGA_ZCTA/MapServer/11/query?where=ZCTA5='{}'&returnGeometry=true&outSR=4326&f=pjson"
zcta = get_zcta("fourthrun",USER, DB_KEY)



async def get_tasks (session, z):
    async with session.get(url.format(z), ssl=False) as session:
        response = await session.json(content_type=None)
        return z, response

async def initialize_table():
    async with aiohttp.ClientSession() as session:
        tasks = [get_tasks(session, z) for z in zcta]   
        results = await asyncio.gather(*tasks)

        for z, response in results:
            bbox = find_bbox(response)
            insertIntoLocations(z, bbox, "fourthrun", USER, DB_KEY)


asyncio.run(initialize_table())









