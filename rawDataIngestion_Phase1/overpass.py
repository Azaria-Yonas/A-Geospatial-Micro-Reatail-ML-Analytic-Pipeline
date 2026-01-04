

def get_overpass_tasks(session, coordinates):
    tasks = []
    url = "https://overpass-api.de/api/interpreter"
    for coor in coordinates:
        query = f"""
        [out:json];
        (
        node["highway"="bus_stop"]({coor[1][0]},{coor[1][1]},{coor[1][2]},{coor[1][3]});
        );
        """
        tasks.append(session.post(url, data={"data": query}))





def get_overpass_task(session, coordinate):
    url = "https://overpass-api.de/api/interpreter"

    query = f"""
        [out:json];
        (
        node["highway"="bus_stop"]({coordinate[0]},{coordinate[1]},{coordinate[2]},{coordinate[3]});
        );
    """
    return session.post(url, data={"data": query})


