import asyncio
import aiohttp


from a_raw_data_ingestion.initialize_data_ingestion.bounding_box import find_bbox
from psql.raw_data.locations import insert_location
from psql.raw_data.zip_code_tabulation_area import get_zcta



url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/PUMA_TAD_TAZ_UGA_ZCTA/MapServer/11/query?where=ZCTA5='{}'&returnGeometry=true&outSR=4326&f=pjson" 
  




async def get_tasks (session, semaphore, z, s): 
    async with semaphore:
        response = None 

        for n in range(8): 
            async with session.get(url.format(z), ssl=False) as resp:
                response = await resp.json(content_type=None)

            if response.get("features"):
                return z, s, response

            await asyncio.sleep(min(10, 1.7 ** n))
            

        return z, s, None 

    

async def initialize_table(zcta, state, func):
    semaphore = asyncio.Semaphore(20) 
    async with aiohttp.ClientSession() as session:
        tasks = [] 
        for i in range(0,len(zcta)): 
            tasks.append(get_tasks(session, semaphore, zcta[i], state[i])) 
             
        for i, coroutine in enumerate(asyncio.as_completed(tasks)): 
            z, s, response = await coroutine
            if response == None:
                func(z, s, None)
                print(f"{i+1}. None: {s}: {z}")
                continue
            bbox = find_bbox(response)
            func(z, s, bbox) 
            print(f"Inserted: {s}: {z} ({i+1}/{len(tasks)})")  



def padd(zcta):
    zcta = list(zcta)
    for i in range(len(zcta)): 
        if len(str(zcta[i])) < 5 : 
            zcta[i] = "0"*(5-len(str(zcta[i]))) + str(zcta[i])

    return zcta 

    



    



if __name__ == "__main__":
    zcta, state = get_zcta() 
    zcta = padd(zcta)
    asyncio.run(initialize_table(zcta, state, insert_location))









