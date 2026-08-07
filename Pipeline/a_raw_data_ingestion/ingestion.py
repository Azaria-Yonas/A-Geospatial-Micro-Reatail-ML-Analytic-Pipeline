import asyncio
import aiohttp
from psql.raw_data.locations import get_coordinates
from a_raw_data_ingestion.places import places_tasks
from a_raw_data_ingestion.overpass import overpass_tasks
from a_raw_data_ingestion.acs import acs_tasks
from a_raw_data_ingestion.arcgis import arcgis_tasks
from a_raw_data_ingestion.cbp_naics import cbp_naics_tasks
from a_raw_data_ingestion.dhc import dhc_tasks  
from psql.raw_data.responses import insert_response



coordinates = get_coordinates() 
state = {coordinate[0]: coordinate[1] for coordinate in coordinates}
 



 

async def ingest_data():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(30)
        # places = [places_tasks(session, coordinate) for  coordinate in coordinates] 
        # overpass = [overpass_tasks(session, coordinate) for  coordinate in coordinates] 
        acs = [acs_tasks(session, coordinate[0], semaphore) for  coordinate in coordinates] 
        arcgis = [arcgis_tasks(session, coordinate[0], semaphore) for  coordinate in coordinates]
        cbp_naics =  [cbp_naics_tasks(session, coordinate[0], semaphore)  for  coordinate in coordinates]
        dhc = [dhc_tasks(session, coordinate[0], semaphore) for coordinate in coordinates]  
        
        results = await asyncio.gather(*acs, *arcgis, *cbp_naics, *dhc, return_exceptions=True)

        for result in results:
            if not isinstance(result, tuple) or len(result) != 4:
                print("Malformed API Response", result)
                continue

            z, r, s, n = result

            if s in (200,204,206):
                insert_response(z, state[z], n, r) 
            
                




if __name__ == "__main__":
    asyncio.run(ingest_data())
