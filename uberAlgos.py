import heapq
import datetime
from helperFuncs import closestNodesDijkstra, find_closest_coordinate
from math import radians


class driver:
    def __init__(self, name, lat, long, time_available):
        
        self.name = name
        self.loc = (lat, long)
        self.time_available = datetime.datetime.strptime(time_available, "%m/%d/%Y %H:%M:%S") - datetime.timedelta(minutes=30)
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.time_available == other.time_available
        return False

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.time_available < other.time_available
        return NotImplemented  # Indicates that the comparison is not implemented for the given types


class passenger:
    def __init__(self, name, startTime, slat, slong, dlat = 0, dlong = 0):
        
        self.name = name
        self.sloc = (slat, slong)
        self.dloc = (dlat, dlong)
        self.startTime = datetime.datetime.strptime(startTime, "%m/%d/%Y %H:%M:%S")
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.startTime == other.startTime
        return False

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.startTime < other.startTime
        return NotImplemented  # Indicates that the comparison is not implemented for the given types



class NotUber:
    def __init__(self):
        self.available_drivers = []
        self.unmatched_passengers = []

    def add_new_driver(self, driver):

        heapq.heappush(self.available_drivers, driver)

    def add_passenger(self, passenger):
        heapq.heappush(self.unmatched_passengers, passenger)

    def match1(self):

        if not self.available_drivers or not self.unmatched_passengers:
            return None

        driver = heapq.heappop(self.available_drivers)
        passenger = heapq.heappop(self.unmatched_passengers)

        return {
            'driver_id': driver.name,
            'driver_obj' : driver,
            'passenger_id': passenger.name,
            'passenger_obj': passenger,
            'available_immediately': NotUber.isAvailable(driver, passenger),
            'matching_alg' : "1"}
    
    @staticmethod
    def isAvailable(driver, passenger):

        #print(driver.time_available <= passenger.startTime)

        return driver.time_available <= passenger.startTime
    
    
    def match2(self, verbose = False):

        if not self.available_drivers or not self.unmatched_passengers:
            return None

    
        passenger = heapq.heappop(self.unmatched_passengers)
        tempDriverAloc = heapq.heappop(self.available_drivers)

        if not NotUber.isAvailable(tempDriverAloc, passenger):

            print("First Element")
            return {
            'driver_id': tempDriverAloc.name,
            'driver_obj' : tempDriverAloc,
            'passenger_id': passenger.name,
            'passenger_obj': passenger,
            'available_immediately': False,
            'matching_alg' : "2"}
        

        minEucDist = distance(tempDriverAloc.loc, passenger.sloc)

        driverCache = []

        
        while len(self.available_drivers) > 0:

            temp = heapq.heappop(self.available_drivers)

            if NotUber.isAvailable(temp, passenger):

                temp_dist = distance(temp.loc, passenger.sloc)
        

                if  temp_dist < minEucDist:

                    driverCache.append(tempDriverAloc)

                    tempDriverAloc = temp
                    minEucDist = temp_dist
                
                else:

                    driverCache.append(temp)

            else:

                heapq.heappush(self.available_drivers, temp)
                break

        
        for i in driverCache:

            heapq.heappush(self.available_drivers, i)

        print("driver available")

        return {
            'driver_id': tempDriverAloc.name,
            'driver_obj' : tempDriverAloc,
            'passenger_id': passenger.name,
            'passenger_obj': passenger,
            'available_immediately': True,
            'matching_alg' : "2"}
    

    def match3_inefficient(self):

        if not self.available_drivers or not self.unmatched_passengers:
            return None

    
        passenger = heapq.heappop(self.unmatched_passengers)
        tempDriverAloc = heapq.heappop(self.available_drivers)

        if not NotUber.isAvailable(tempDriverAloc, passenger):

            print("First Element")
            return {
            'driver_id': tempDriverAloc.name,
            'driver_obj' : tempDriverAloc,
            'passenger_id': passenger.name,
            'passenger_obj': passenger,
            'available_immediately': False,
            'matching_alg' : "3 inefficient"}
        

        minTravelTime = closestNodesDijkstra(tempDriverAloc.loc, passenger.sloc, passenger.startTime)

        driverCache = []

        
        while len(self.available_drivers) > 0:

            temp = heapq.heappop(self.available_drivers)

            if NotUber.isAvailable(temp, passenger):

                temp_time = closestNodesDijkstra(temp.loc, passenger.sloc, passenger.startTime)
        

                if  temp_time < minTravelTime:

                    driverCache.append(tempDriverAloc)

                    tempDriverAloc = temp
                    minTravelTime = temp_time
                
                else:

                    driverCache.append(temp)

            else:

                heapq.heappush(self.available_drivers, temp)
                break

        
        for i in driverCache:

            heapq.heappush(self.available_drivers, i)


        return {
            'driver_id': tempDriverAloc.name,
            'driver_obj' : tempDriverAloc,
            'passenger_id': passenger.name,
            'passenger_obj': passenger,
            'available_immediately': True,
            'matching_alg' : "3 inefficient"}
    
    def match3_efficient(self):

        if not self.available_drivers or not self.unmatched_passengers:
            return None

    
        passenger = heapq.heappop(self.unmatched_passengers)
        tempDriverAloc = heapq.heappop(self.available_drivers)

        if not NotUber.isAvailable(tempDriverAloc, passenger):

            print("First Element")
            return {
            'driver_id': tempDriverAloc.name,
            'driver_obj' : tempDriverAloc,
            'passenger_id': passenger.name,
            'passenger_obj': passenger,
            'available_immediately': False,
            'matching_alg' : "3 efficient"}
        

        driverCache = []

        shortestPaths = closestNodesDijkstra(passenger.sloc, None, passenger.startTime)

        startCoord = {'lat': tempDriverAloc.loc[0], 'lon': tempDriverAloc.loc[1]}

        minTravelTime = shortestPaths[int(find_closest_coordinate(startCoord))]

        
        while len(self.available_drivers) > 0:

            temp = heapq.heappop(self.available_drivers)
            if NotUber.isAvailable(temp, passenger):

                coord = {'lat': temp.loc[0], 'lon': temp.loc[1]}

                temp_time = shortestPaths[int(find_closest_coordinate(coord))]
        

                if  temp_time < minTravelTime:

                    driverCache.append(tempDriverAloc)

                    tempDriverAloc = temp
                    minTravelTime = temp_time
                
                else:

                    driverCache.append(temp)

            else:

                heapq.heappush(self.available_drivers, temp)
                break

        
        for i in driverCache:

            heapq.heappush(self.available_drivers, i)


        return {
            'driver_id': tempDriverAloc.name,
            'driver_obj' : tempDriverAloc,
            'passenger_id': passenger.name,
            'passenger_obj': passenger,
            'available_immediately': True,
            'matching_alg' : "3 efficient"}

    def match4():
        class Node:
            def __init__(self, id, cost):
                self.id = id
                self.cost = cost
                self.g = float('inf')  # Distance from start node
                self.h = 0  # Heuristic estimate to goal node
                self.parent = None

            def __lt__(self, other):
                return (self.g + self.h) < (other.g + other.h)
            
        class KdNode:
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

            return KdNode(
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

            with open("data/node_data.csv", 'r') as file:
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

        def heuristic(node, goal):
            return abs(node.cost - goal.cost)


        def astar(graph, start_id, goal_id):
            start_node = Node(start_id, graph[start_id].cost)
            goal_node = Node(goal_id, graph[goal_id].cost)

            open_set = []
            closed_set = set()

            heapq.heappush(open_set, start_node)

            while open_set:
                current_node = heapq.heappop(open_set)

                if current_node.id == goal_node.id:
                    path = []
                    while current_node:
                        path.append((current_node.id, current_node.cost))
                        current_node = current_node.parent
                    return path[::-1]

                closed_set.add(current_node.id)

                for neighbor_id, edge_cost in graph[current_node.id].neighbors.items():
                    if neighbor_id not in closed_set:
                        neighbor = Node(neighbor_id, edge_cost)
                        neighbor.g = current_node.g + edge_cost
                        neighbor.h = heuristic(neighbor, goal_node)
                        neighbor.parent = current_node

                        if neighbor not in open_set:
                            heapq.heappush(open_set, neighbor)

            return None  # No path found

    
    def match5(self, max_distance=5.0, verbose=False):
        if not self.available_drivers or len(self.unmatched_passengers) < 2:
            return None

        passenger1 = heapq.heappop(self.unmatched_passengers)
        passenger2 = heapq.heappop(self.unmatched_passengers)

        # Check if the two passengers are within a set distance of each other
        distance_between_passengers = distance(passenger1.sloc, passenger2.sloc)
        if distance_between_passengers <= max_distance:
            # Try to find a driver who can serve both passengers
            tempDriverAloc = heapq.heappop(self.available_drivers)

            minEucDist = distance(tempDriverAloc.loc, passenger1.sloc) + distance(tempDriverAloc.loc, passenger2.sloc)

            # Check if the driver can serve both passengers within a set distance
            if minEucDist <= max_distance:
                if not NotUber.isAvailable(tempDriverAloc, passenger1):
                    print("First Element")
                    return {
                        'driver_id': tempDriverAloc.name,
                        'driver_obj': tempDriverAloc,
                        'passenger_id': [passenger1.name, passenger2.name],
                        'passenger_obj': [passenger1, passenger2],
                        'available_immediately': False,
                        'matching_alg' : "5"
                    }
                # # Update driver location and time based on serving both passengers
                # recycled_driver = tempDriverAloc
                # recycled_driver.time_available = max(passenger1.startTime, passenger2.startTime) + datetime.timedelta(
                #     hours=minEucDist)
                # recycled_driver.loc = passenger2.dloc
                # profit = (distance(tempDriverAloc.loc, passenger2.dloc) * 60) - (minEucDist * 60)
                # profit_list.append(profit)
                # passengers_waiting_list.append(minEucDist * 60)

                print("Driver available for both passengers")
                return {
                    'driver_id': tempDriverAloc.name,
                    'driver_obj': tempDriverAloc,
                    'passenger_id': [passenger1.name, passenger2.name],
                    'passenger_obj': [passenger1, passenger2],
                    'available_immediately': True,
                    'matching_alg' : "5"
                }
            

        # If the passengers are not within the set distance, match each passenger with the closest available driver individually
        heapq.heappush(passenger1)
        heapq.heappush(passenger2)
        return self.match2()
    


def find_time(start_location, end_location):
    return distance(start_location, end_location)

def distance(location1, location2):


    R = 6373.0

    lat1 = radians(location1[0])
    lon1 = radians(location1[1])
    lat2 = radians(location2[0])
    lon2 = radians(location2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    distance = ((dlon) ** 2 + (dlat ** 2)) ** 0.5

    return distance



if __name__ == "__main__":

    test = NotUber()

    test.add_new_driver(driver("billy", 40.66, -77.39, "04/20/2014 00:00:00"))
    test.add_new_driver(driver("Nob", 40.68, -77.38, "04/21/2014 00:00:00"))

    test.add_passenger(passenger("Sam","04/25/2014 00:00:00", 40.68, -77.38))

    print(test.match2()) #Match


    test.add_passenger(passenger("Taylor","04/26/2014 00:00:00", 40.66, -77.40))

    print(test.match2()) #Match

    test.add_passenger(passenger("Tom","04/25/2014 00:00:00", 40.66, -77.430))

    print(test.match2()) #None

    test.add_passenger(passenger("Emma Stone","04/25/2014 00:00:00", 40.88, -77.42))

    print(test.match2()) #None

    test.add_passenger(passenger("Dom","04/25/2014 00:00:00", 40.66, -79.40))

    print(test.match2()) #None

    test.add_new_driver(driver("john", 40.88, -77.42, "04/25/2014 00:00:00"))

    print(test.match2()) #Match John to Emma
