

def find_bbox(data):
    rings = data["features"][0]["geometry"]["rings"]

    if not rings: 
        return None
    
    minLat = 90
    maxLat = -90

    minLong = 180
    maxLong = -180

    for ring in rings:
        for long, lat in ring:

            maxLat = max(maxLat, lat)
            minLat = min(minLat, lat)

            minLong = min(minLong, long)
            maxLong = max(maxLong, long)


    return (minLat, minLong, maxLat, maxLong)



# I found an API, TIGERWeb, that returns coordinates which map Zip Code Tabulation Areas (ZCTAs).
# It returns a JSON containing longitude–latitude pairs. However, to my inconvenience,
# there are thousands of these pairs that precisely bound a given ZCTA. For APIs like
# Places, this exceeds request limits, and they are also difficult to store and load
# into memory, along with other related overhead.
# Therefore, I came up with an algorithm that locates the extreme points.
# This forms a bounding box.
# This isn’t the most accurate approach, but I figured that most ZCTAs look
# roughly like boxes, so this works well enough.
    
