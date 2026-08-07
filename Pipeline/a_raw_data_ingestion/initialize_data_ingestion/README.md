

# Pipeline/a_raw_data_ingestion/initialize_data_ingestion

- This sub directory is for initiating the raw data ingestion. Things such as creating the schema, arranging the ZCTAs, and calculating the bounding boxes are done here.


## FILES


### Tables 

#### 1. SQL/zip_code_tabulation_area.sql

- This is the table that I will be storing the ZIP Code Tabulation Areas

#### 2. Locations

- In this table I store thing such as coordinates, which are very useful for making api calls as some of the API endpoints don't take the raw ZCTA's as a parameter.
- The coordinates of the zcta are mapped into and stored as bounding boxes. I also used the bounding box to generate a point and radius, which works as estimate when both zcta and bounding boxes aren't available as a parameter.



### Scripts

#### 1. fetch_zcta.py

- Initially I was Cluster sampling (I chose cities such as LA and Seattle to make predictions Nation wide) however now I am using a Stratified Random Sampling over each state. As a result it would be very difficult to type down around 10,000 ZCTAs into a INSERT query. This file is a script that fetches all the ZCTA state by state and random picks one third. This will be my sample.


#### 2. initialize_loactions.py

- APIs such as Places and Overpass don't take ZCTA as a parameter. As a result, I use another api called TigerWEB in order to get the statelite mapping of each ZCTA so I can get geo spactial socio-economic variables from the Places and Overpass API. 

- One issue I kept running into was that the TigerWEB API was quickly overwhelmed with the many asychronous requests being sent. As a result, most of the ten thousand requests timed out, failed, or didn't return expected data. Initially, while I was working with only a couple hundred samples this wasn't much of a problem and the solution was to query a few ZCTAs at a time and manually adjust the query to get the next set of ZCTAs. However, as I scaled this experiment, this method became ineffective. I tried switching over to synchronous code, however that was taking too long. The solution was simple, I added rate limiter and automatic retries. This minimized the amount of bad responses while being incredibly fast. I still did get a few bad responses but I handled them in retry_locations.py.


#### 3. bounding_box.py

- The TigerWEB API endpoint returns a dictionary of tens of thousands of coordinates precisely mapping all the streets, roads, and builds that are included in that ZCTA. However I found that storing the bounding boxes is better as the values of the variables are roughly the same while being easier to work with. Therefore, I used a simple algorithm to pull the extremes (minLat, minLong, maxLat, maxLong).


#### 4. retry_locations.py

- This file imports the central function, initialize_table, from initialize_locations.py and loads it with all the ZCTAs that returned anything other than the expected output (coordinates). And instead of the insert query this function is invoked with the update query to go ahead and replace bad responses with the retries.








