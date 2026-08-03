import time
import requests
import random

from psql.raw_data.zip_code_tabulation_area import load_zcta
from config import CENSUS


URL = "https://api.census.gov/data/2020/dec/dhc" 




STATE_CODES = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06",
    "CO": "08", "CT": "09", "DE": "10", "DC": "11", "FL": "12",
    "GA": "13", "HI": "15", "ID": "16", "IL": "17", "IN": "18",
    "IA": "19", "KS": "20", "KY": "21", "LA": "22", "ME": "23",
    "MD": "24", "MA": "25", "MI": "26", "MN": "27", "MS": "28",
    "MO": "29", "MT": "30", "NE": "31", "NV": "32", "NH": "33",
    "NJ": "34", "NM": "35", "NY": "36", "NC": "37", "ND": "38",
    "OH": "39", "OK": "40", "OR": "41", "PA": "42", "RI": "44",
    "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49",
    "VT": "50", "VA": "51", "WA": "53", "WV": "54", "WI": "55",
    "WY": "56",
}


def get_params(code): 
    return {
        "get": "NAME", 
        "for": "zip code tabulation area:*",
        "in": f"state:{code}",
        "key": CENSUS, 
         
    } 




def rand(array):
    x = array        
    random.shuffle(x) 
    return x[:len(x) // 3] 


def get_distribution():
     
    res = []
    for state, code in STATE_CODES.items():
        response = requests.get(URL, params=get_params(code)) 

        if response.status_code != 200:
            print(state, response.status_code, response.text) 
            continue 

        data = response.json()
        rows = data[1:]
        res = [row[2] for row in rows] 

        load_zcta(state, rand(res)) 

        time.sleep(0.2) 
         


if __name__ == "__main__": 
    get_distribution() 

     














