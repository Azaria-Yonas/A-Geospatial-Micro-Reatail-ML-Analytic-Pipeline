import asyncio
import aiohttp

from psql.coordinates import get_coordinates
from a_raw_data_ingestion.places import places_tasks
from a_raw_data_ingestion.overpass import overpass_tasks
from a_raw_data_ingestion.census import census_tasks
from a_raw_data_ingestion.arcgis import arcgis_tasks       ### You need to find a way to filter errors

                                      ### Also need to create a way to retry tasks especially for 500 errors
                                      ### And I need to end the event loop if I get a 400 error


coordinates = get_coordinates(hbound=1)

for i in range(len(coordinates)):
    print (f"{i+1} :  {coordinates[i]}")





# async def ingest_data():
#     async with aiohttp.ClientSession() as session:
#         places = [places_tasks(session, coordinate) for  coordinate in coordinates] 
#         overpass = [overpass_tasks(session, coordinate) for  coordinate in coordinates] 
#         census = [census_tasks(session, coordinate) for  coordinate in coordinates] 
#         arcgis = [arcgis_tasks(session, coordinate) for  coordinate in coordinates] 

#         results = await asyncio.gather(*places, *overpass, *census, *arcgis, return_exceptions=True)

#         for item in results:
#             if isinstance(item, Exception):
#                 print("TASK FAILED:", repr(item))
#                 continue
#             z, r, s = item
#             print(f"{z}->{s}:\n\n{r}")



# if __name__ == "__main__":
#     asyncio.run(ingest_data())
