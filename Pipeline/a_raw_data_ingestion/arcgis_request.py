import asyncio
import aiohttp
import json
import os
from psql.raw_data.requests import insert_request
from psql.raw_data.responses import insert_response
from config import ARGIS


URL = "https://geoenrich.arcgis.com/arcgis/rest/services/World/GeoEnrichmentServer/GeoEnrichment/enrich" 




def get_body(zcta):
    return {
        "f": "json",
        "token": ARGIS,  
        "studyAreas": json.dumps([{
            "sourceCountry": "US",
            "layer": "US.ZIP5", 
            "ids": [str(zcta)]
        }]),
        "analysisVariables": ",".join([
            "AgeDependency.CHILD_CY",           # 2026 Child Population 
            "AgeDependency.WORKAGE_CY",         # 2026 Working Population 
            "AgeDependency.SENIOR_CY",          # 2026 Senior Population
            # "AgeDependency.CHLDDEP_CY",         # 2026 Child Dependency Ratio               ---> Noise
            # "AgeDependency.AGEDEP_CY",          # 2026 Age Dependency Ratio                 ---> Noise
            # "AgeDependency.SENRDEP_CY",         # 2026 Senior Dependency Ratio               ---> Noise
            # "AgeDependency.CHILD_FY",           # 2031 Child Population                   ---> Already have 2026 child population dont need this projection
            # "AgeDependency.WORKAGE_FY",         # 2031 Working-Age Population                 ---> skip this
            # "AgeDependency.SENIOR_FY",          # 2031 Senior Population                            ---> These are just projections
            # "AtRisk.TOTPOP_CY",                 # 2026 Total Population                   ---> new variable put in decennial_request.py P1_001N)
            # "AtRisk.GQPOP_CY",                  # 2026 Group Quarters Population          ---> not sure how useful
            # "AtRisk.TOTHH_CY",                  # 2026 Total Households                   ---> new variable put in census_request.py B11001_001E
            # "AtRisk.AVGHHSZ_CY",                # 2026 Average Household Size             ---> new variable put in decennial_request.py H8_001N / H9_001N
            # "AtRisk.AVGHINC_CY",                # 2026 Average Household Income           ---> new variable put in census_request.py B19025_001E / B11001_001E
            # "AtRisk.MP01001h_B",                # 2026 HH Owns or Leases 1+ Vehicles          ---> new variable put in census_request.py B25044 totals minus no-vehicle counts)
            "crime.CRMCYTOTC",                  # 2026 Total Crime Index                        ---> Total crime and 
            # "crime.CRMCYPERC",                  # 2026 Personal Crime Index                          ---> Might be redundant
            "DaytimePopulation.DPOP_CY",        # 2026 Total Daytime Population
            "DaytimePopulation.DPOPWRK_CY",     # 2026 Daytime Pop: Workers
            # "DaytimePopulation.DPOPRES_CY",     # 2026 Daytime Pop: Residents                        ---> I Could get a good estimate on this by subtracting day time workers with the total population
            "DaytimePopulation.DPOPDENSCY",     # 2026 Daytime Pop Density
            "disposableincome.MEDDI_CY",        # 2026 Median Disposable Income
            "disposableincome.AVGDI_CY",        # 2026 Average Disposable Income
            # "disposableincome.AGGDI_CY",        # 2026 Aggregate Disposable Income            ---> git the mean and median so might not be worth the cost for me
            "education.X11002_A",               # 2026 Avg: College Tuition
            "financial.X14058_A",               # 2026 Avg: Value of Stocks
            # "financial.X14058_I",               # 2026 Index: Value of Stocks
            "homevalue.MEDVAL_CY",              # 2026 Median Home Value
            "homevalue.AVGVAL_CY",              # 2026 Average Home Value
            # "homevalue.MEDVAL_FY",              # 2031 Median Home Value                            ---> These are projections so we can leave them out
            # "homevalue.AVGVAL_FY",              # 2031 Average Home Value                           ---> Same rule
            # "householdincome.MEDHINC_CY",       # 2026 Median Household Income                    ---> new variable put in census_request.py B19013_001E
            # "householdincome.AVGHINC_CY",       # 2026 Average Household Income                     ---> new variable put in census_request.py B19025_001E / B11001_001E
            # "householdincome.PCI_CY",           # 2026 Per Capita Income                                ---> new variable put in census_request.py B19301_001E
            # "householdsbysize.AVGHHSZ20",       # 2020 Average Household Size                       ---> new variable put in decennial_request.py H8_001N / H9_001N
            # "householdtotals.TOTHH_CY",         # 2026 Total Households                                 ---> new variable put in census_request.py B11001_001E
            # "householdtotals.AVGHHSZ_CY",       # 2026 Average Household Size                       ---> new variable put in decennial_request.py H8_001N / H9_001N
            "networth.MEDNW_CY",                # 2026 Median Net Worth
            "networth.AVGNW_CY",                # 2026 Average Net Worth
            # "networth.AGGNW_CY",                # 2026 Aggregate Net Worth                          ---> Average and Median are sufficient
        ]),
        "returnGeometry": "false"
    }



async def arcgis_tasks(session,zcta):
    body = get_body(zcta)

    async with session.post(URL, data=body) as resp:
        status = resp.status
        try:
            response = await resp.json(content_type=None)        
            insert_request(zcta, "arcgis", URL, "POST", body=body, status_code=status) 
        except aiohttp.ContentTypeError:
            response = await resp.text() 
            insert_request(zcta, "arcgis", URL, "POST", body=body, status_code=status, error_message=response ) 
        return zcta, response, status, "arcgis"













###########################################
###                                     ###
###  This here is to test individually  ###
###                                     ###
###########################################



# async def func(coordinate):
#     async with aiohttp.ClientSession() as session:
#         tasks = [arcgis_tasks(session,  coordinate[0])]
#         results = await asyncio.gather(*tasks)
#         for z ,r, s, n in results:
#             if s == 200:
#                 print(r)
#                 insert_response(z, "test", "arcgis", r)  


# coordinates = ( 98103, (47.6031739999818, -122.3512549998386, 47.61851099976298, -122.32135299996169), (47.61084249987239,-122.33630399990014,1409.8593630867806))

# if __name__ == "__main__":
#     asyncio.run(func(coordinates))