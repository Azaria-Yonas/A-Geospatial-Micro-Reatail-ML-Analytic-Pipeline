import asyncio
import aiohttp
import os
from coordinates import get_coordinates   # ('zip', '(l,-l,l,-l)', '("(l,-l)",radius)')
from places import get_places_task
from overpass import get_overpass_task




PLACES_KEY = os.getenv("PLACES_API_KEY")
ARCGIS_KEY = os.getenv("ArcGIS")

DB_USERNAME = os.getenv("psqlUser")
DB_PASSWORD = os.getenv("dbKEY")


coordinates = get_coordinates("thirdrun", DB_USERNAME, DB_PASSWORD) 



def nested_tasks(session, coordinates):
    tasks = {}

    for coor in coordinates:
        tasks[coor[0]] = (get_overpass_task(session, coor[1]), get_places_task(session, coor[2], PLACES_KEY))






