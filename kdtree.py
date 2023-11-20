class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

def build_kd_tree(points, depth=0):
    if len(points) == 0:
        return None

    axis = depth % 2 #alternates between 0 and 1
    #each level of the tree should be sorted by lon then lat alternating
    points_sorted = sorted(points, key=lambda x: x[axis]) #sorts based on alternating axes
    mid = len(points_sorted) // 2

    return Node(
        point=points_sorted[mid],
        left=build_kd_tree(points_sorted[:mid], depth + 1),
        right=build_kd_tree(points_sorted[mid + 1:], depth + 1)
    )

def find_nearest_neighbor(node, target, depth=0):
    if node is None:
        return None

    k = len(target)
    axis = depth % k

    next_branch = None
    opposite_branch = None

    if target[axis] < node.point[axis]:
        next_branch = node.left
    else:
        next_branch = node.right

    next_depth = depth + 1 if next_branch == node.left else depth
    next_best = find_nearest_neighbor(next_branch, target, next_depth)

    best = node.point
    best_distance = distance(target, node.point)

    if next_best is not None:
        next_best_distance = distance(target, next_best)
        if next_best_distance < best_distance:
            best = next_best
            best_distance = next_best_distance

    if abs(target[axis] - node.point[axis]) < best_distance:
        opposite_branch = node.right if next_branch == node.left else node.left
        opposite_best = find_nearest_neighbor(opposite_branch, target, depth + 1)

        if opposite_best is not None:
            opposite_best_distance = distance(target, opposite_best)
            if opposite_best_distance < best_distance:
                best = opposite_best

    return best

def distance(location1, location2):

    from math import sin, cos, sqrt, atan2, radians

    R = 6373.0
    
    #longitude is hosted in index 0, latitude is in index 1
    lat1 = radians(location1[1])
    lon1 = radians(location1[0])
    lat2 = radians(location2[1])
    lon2 = radians(location2[0])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    # distance = abs(dlon) + abs(dlat)
    # distance = ((dlon) ** 2 + (dlat ** 2)) ** 0.5
    return distance

def read_coordinates():
    import json

    with open("data/node_data.json", 'r') as file:
        data = json.load(file)
    return data

coordinates_data = read_coordinates()

# print(coordinates_data)

input_lon = -73.935242
input_lat = 40.655865

# converting to list so i can use 0, 1 values
coordinates_list = [list(coord.values()) for coord in coordinates_data.values()]

kd_tree = build_kd_tree(coordinates_list)
nearest_neighbor = find_nearest_neighbor(kd_tree, [input_lon, input_lat])

print(f"The key with coordinates closest to ({input_lon}, {input_lat}) is: {nearest_neighbor}")