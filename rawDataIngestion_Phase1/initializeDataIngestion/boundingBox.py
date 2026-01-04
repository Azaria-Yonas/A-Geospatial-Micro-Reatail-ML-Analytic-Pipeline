

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



# I found an api, TIGERWeb, that returns coordinates that map zcta. It 
# returns a JSON contaning logitude-latitude pairs. However, to my inconvience,
# zcta
