

def get_places_tasks(sessions, coordinates, api_key):
    URL = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key":   api_key,
            "X-Goog-FieldMask": "places.displayName"
    }
    tasks = []
    for coor in coordinates:
        body = {
            "includedPrimaryTypes": ["barber_shop"],
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": coor[2][0][0], "longitude": coor[2][0][1]},
                    "radius": coor[2][1]
                }
            }
        }

        tasks.append(sessions.post(url=URL, headers=headers, json=body))



        



