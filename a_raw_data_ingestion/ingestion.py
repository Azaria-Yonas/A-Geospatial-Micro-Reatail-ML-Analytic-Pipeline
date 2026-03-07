import asyncio
import aiohttp

from psql.coordinates import get_coordinates
from a_raw_data_ingestion.places import places_tasks
from a_raw_data_ingestion.overpass import overpass_tasks
from a_raw_data_ingestion.census import census_tasks
from a_raw_data_ingestion.arcgis import arcgis_tasks       
from psql.responses import insert_response




coordinates, city = get_coordinates(lbound=25, hbound=30)



for i in range(len(coordinates)):
    print (f"{i+1} :  {coordinates[i]}")
    print(city)



async def ingest_data():
    async with aiohttp.ClientSession() as session:
        # places = [places_tasks(session, coordinate) for  coordinate in coordinates] 
        # overpass = [overpass_tasks(session, coordinate) for  coordinate in coordinates] 
        census = [census_tasks(session, coordinate[0]) for  coordinate in coordinates] 
        arcgis = [arcgis_tasks(session, coordinate[0]) for  coordinate in coordinates] 

        results = await asyncio.gather(*census, *arcgis, return_exceptions=True)

        for result in results:
            if not isinstance(result, tuple) or len(result) != 4:
                print("Malformed result:", result)
                continue

            z, r, s, n = result

            if s == 200:
                insert_response(z, city, n, r)



if __name__ == "__main__":
    asyncio.run(ingest_data())
