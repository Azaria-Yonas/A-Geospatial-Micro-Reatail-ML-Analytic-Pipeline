import os
from dotenv import load_dotenv

load_dotenv(".env/.env") 


# Postgres Credentials:
DB_KEY = os.getenv("DB_KEY")
USERNAME = os.getenv("USERNAME")          
DATABASE = os.getenv("DATABASE") 


# API Keys:
PLACES = os.getenv("PLACES_KEY")
ARGIS = os.getenv("ARGIS_KEY")  
CENSUS = os.getenv("CENSUS_KEY") 






