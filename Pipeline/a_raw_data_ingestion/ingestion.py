import asyncio
import aiohttp
from psql.raw_data.coordinates import get_coordinates
from a_raw_data_ingestion.places_request import places_tasks
from a_raw_data_ingestion.overpass_request import overpass_tasks
from Pipeline.a_raw_data_ingestion.acs import acs_tasks
from Pipeline.a_raw_data_ingestion.arcgis import arcgis_tasks
from Pipeline.a_raw_data_ingestion.cbp_naics import cbp_tasks
from Pipeline.a_raw_data_ingestion.dhc import dhc_tasks  
from psql.raw_data.responses import insert_response




coordinates, city = get_coordinates(lbound=100, hbound=109)



for i in range(len(coordinates)):
    print (f"{i+1}. {city}  {coordinates[i]}")



async def ingest_data():
    async with aiohttp.ClientSession() as session:
        # places = [places_tasks(session, coordinate) for  coordinate in coordinates] 
        # overpass = [overpass_tasks(session, coordinate) for  coordinate in coordinates] 
        acs = [acs_tasks(session, coordinate[0]) for  coordinate in coordinates] 
        arcgis = [arcgis_tasks(session, coordinate[0]) for  coordinate in coordinates]
        cbp =  [cbp_tasks(session, coordinate[0])  for  coordinate in coordinates]
        dhc = [dhc_tasks(session, coordinate[0]) for coordinate in coordinates]  
        
        results = await asyncio.gather(*acs, *arcgis, *cbp, *dhc, return_exceptions=True)

        for result in results:
            if not isinstance(result, tuple) or len(result) != 4:
                print("Malformed API Response", result)
                continue

            z, r, s, n = result

            if s in (200,204,206):
                insert_response(z, city, n, r)
                




if __name__ == "__main__":
    asyncio.run(ingest_data())
