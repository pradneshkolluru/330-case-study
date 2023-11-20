def read_coordinates():
    import json

    with open("data/node_data.json", 'r') as file:
        data = json.load(file)
    return data

coordinates = read_coordinates()

# for i, (key, value) in enumerate(coordinates.items()):
#     if i < 5:
#         print(f"{key}: {value}")
#     else:
#         break

# print(coordinates["42467333"])
# print(coordinates["42467333"]["lon"])
# print(coordinates["42467333"]["lat"])
# print(type(coordinates["42467333"]["lon"]))

#calculate distance
def distance(location1, location2):

    from math import sin, cos, sqrt, atan2, radians

    R = 6373.0

    lat1 = radians(location1["lat"])
    lon1 = radians(location1["lon"])
    lat2 = radians(location2["lat"])
    lon2 = radians(location2["lon"])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def find_closest_coordinate(target_coord, coordinates):
    min_distance = float('inf') #big maximum
    closest_node = None

    for key, coords in coordinates.items():
        dist = distance(target_coord, coords)
        if dist < min_distance:
            min_distance = dist
            closest_node = key

    print(min_distance)
    return closest_node

# Example usage:
input_coordinates = {'lon': -73.935242, 'lat': 40.655865}

closest_coord = find_closest_coordinate(input_coordinates, coordinates)
print(f"The closest coordinate to {input_coordinates} is {closest_coord, coordinates[closest_coord]}.")








