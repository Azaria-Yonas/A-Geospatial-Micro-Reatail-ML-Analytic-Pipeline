import os
from dotenv import load_dotenv

load_dotenv(".env/.env") 


# Postgres Credentials:
PSQL_KEY = os.getenv("DB_KEY")
PSQL_USER = os.getenv("USERNAME")          


# API Keys:
PLACES = os.getenv("PLACES_KEY")
ARGIS = os.getenv("ARGIS_KEY")  
CENSUS = os.getenv("CENSUS_KEY") 






