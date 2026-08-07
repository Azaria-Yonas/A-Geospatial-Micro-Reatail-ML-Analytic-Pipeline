
# Pipeline/a_raw_data_ingestion/

- This sub directory is where all the raw data is ingested from the API endpoints. The data at this stage is unflitered and stored as JSON. In addtion, inside the 

- In a_raw_data_ingestion/initialize_data_ingestion there is more information on how data ingestion was initialized, how ZCTA were sampled and much more.

## FILES


### Tables 

#### 1. SQL/responses.sql

- This table is where the raw api responses are stored. The responses are indexed based on the US State, time, and API



#### 2. SQL/requests.sql 


- I created this table because the information it stored needed to be separated from the responses table. Keeping both successful and failed requests in the same table made the pipeline difficult to maintain, as the table contained a mix of different types of responses. Initially while I had both tabled in union, it resulted in esulted in unnecessary storage overhead because some columns were only relevant for successful requests while others where only relevant for error requests, leaving many entries empty. This made quering difficult and indexing heavy. Separating them allowed me to store the relvant information for successful reqeusts separately in the requests table, making it simpler and easier to work with.


- On the other hand, the requests table keeps track of all the requests being sent. It stores the details needed to view and debug bad requests, including status codes, error messages, as well as elements of the request itself, such as the headers, request body, method, and endpoint. 

### Scripts 


#### 1. Pipeline/a_raw_data_ingestion/acs.py 

- This script fetches variables from the American Community Survey dataset of the US Census. 



#### 2. Pipeline/a_raw_data_ingestion/arcgis.py

- This script fetches  Ersi's Geoenrichment variables through their software platfrom ArcGIS.



#### 3. Pipeline/a_raw_data_ingestion/cbp-naics.py
- This script fetches variables from the North American Industry Classification System and County Business Patterns dataset of the US Census. 



#### 4. Pipeline/a_raw_data_ingestion/dhc.py
- This script fetches variables from the Demographic and Housing Characteristics dataset of the US Census.



#### 5. Pipeline/a_raw_data_ingestion/places.py
- This script fetches business aggregates from Googles Places API.



#### 6. Pipeline/a_raw_data_ingestion/overpass.py
- This script fetches road network data from OpenStreetMap.

#### 7. Pipeline/a_raw_data_ingestion/ingest.py
- This script gathers all the requests from all the APIs and send them of together















