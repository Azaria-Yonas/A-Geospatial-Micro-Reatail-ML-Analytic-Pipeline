import asyncio
import aiohttp


from a_raw_data_ingestion.initialize_data_ingestion.bounding_box import find_bbox
from psql.locations import insert_location
from psql.zip_code_tabulation_area import get_zcta



url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/PUMA_TAD_TAZ_UGA_ZCTA/MapServer/11/query?where=ZCTA5='{}'&returnGeometry=true&outSR=4326&f=pjson"



zcta = get_zcta(lbound=30)



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
            insert_location(z, bbox)


asyncio.run(initialize_table())









