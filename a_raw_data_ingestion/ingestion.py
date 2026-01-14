import asyncio
import aiohttp

from psql.coordinates import get_coordinates
from places import places_tasks
from overpass import overpass_tasks
from census import census_tasks
from arcgis import arcgis_tasks       ### You need to find a way to filter errors

                                      ### Also need to create a way to retry tasks especially for 500 errors
                                      ### And I need to end the event loop if I get a 400 error


coordinates = get_coordinates()


async def ingest_data():
    async with aiohttp.ClientSession() as session:
        places = [places_tasks(session, coordinate) for  coordinate in coordinates] 
        overpass = [overpass_tasks(session, coordinate) for  coordinate in coordinates] 
        census = [census_tasks(session, coordinate) for  coordinate in coordinates] 
        arcgis = [arcgis_tasks(session, coordinate) for  coordinate in coordinates] 

        results = await asyncio.gather(*places, *overpass, *census, *arcgis)

        for z, r, s in results:
            print(f"{z}->{s}: \n\n\n\n {r}")



if __name__ == "__main__":
    asyncio.run()
