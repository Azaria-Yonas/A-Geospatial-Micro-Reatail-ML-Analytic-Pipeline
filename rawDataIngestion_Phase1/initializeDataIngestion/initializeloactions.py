import os
import asyncio
import aiohttp


from zipcodes import get_zipcodes
from boundingBox import find_bbox
from insert import insertIntoLocations

DB_KEY = os.getenv("dbKey")
USER = os.getenv("psqlUser")
url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/PUMA_TAD_TAZ_UGA_ZCTA/MapServer/11/query?where=ZCTA5='{}'&returnGeometry=true&outSR=4326&f=pjson"
zipCodes = get_zipcodes("thirdrun",USER, DB_KEY)



def get_tasks (session):
    tasks = {} 
    for zip in zipCodes:
        tasks[zip] = session.get(url.format(zip), ssl=False)
    return tasks

async def func():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks.values())
        for i in range(len(responses)):
            coor = find_bbox(await responses[i].json(content_type=None))
            insertIntoLocations(zipCodes[i], coor, "thirdrun", USER, DB_KEY)    

asyncio.run(func())









