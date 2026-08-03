import time
import requests
import random
from collections import defaultdict
from psql.raw_data.zip_code_tabulation_area import load_zcta
from config import CENSUS 



URL_API = "https://api.census.gov/data/2010/dec/sf1" 
URL_REL = "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt" 






STATE_CODES_REVERSE = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA",
    "08": "CO", "09": "CT", "10": "DE", "11": "DC", "12": "FL",
    "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN",
    "19": "IA", "20": "KS", "21": "KY", "22": "LA", "23": "ME",
    "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS",
    "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
    "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND",
    "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI",
    "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT",
    "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI",
    "56": "WY",
} 




def get_zcta_state_crosswalk(): 

    response = requests.get(URL_REL)


    response.raise_for_status()

    
    zcta_to_states = defaultdict(set)

    lines = response.text.strip().split('\n')

    header = lines[0].split(',')
    
    zcta_idx = header.index("ZCTA5")
    state_idx = header.index("STATE")
    
    
    for line in lines[1:]: 
        parts = line.split(',')
        if len(parts) > state_idx: 
            zcta = parts[zcta_idx]
            state_fips = parts[state_idx]
            state_abbr = STATE_CODES_REVERSE.get(state_fips)
            
            if state_abbr:
                zcta_to_states[zcta].add(state_abbr)
                
    return zcta_to_states 


 



def rand(array):
    x = array        
    random.shuffle(x) 
    return x[:len(x) // 3] 


def get_distribution(): 
    crosswalk = get_zcta_state_crosswalk() 
     
    
    params = {
        "get": "NAME",
        "for": "zip code tabulation area:*",
        "key": CENSUS,
    }

    response = requests.get(URL_API, params=params)

    if response.status_code != 200:
        return 

    data = response.json()
    if len(data) < 2: 
        return
      

  
    state_to_api_zctas = defaultdict(list)
     
    rows = data[1:]   
    for row in rows: 
        zcta = row[1] 
        
        
        states_for_zcta = crosswalk.get(zcta, set())
        
        for state_abbr in states_for_zcta: 
            state_to_api_zctas[state_abbr].append(zcta)  
             

    
    for state, zctas in state_to_api_zctas.items():
        load_zcta(state, rand(zctas))
        time.sleep(0.2)
         

if __name__ == "__main__":
    get_distribution()











