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
            def __init__(self, row, col):
                self.row = row
                self.col = col
                self.g = 0
                self.h = 0
                self.parent = None

            def __lt__(self, other):
                return (self.g + self.h) < (other.g + other.h)

        def heuristic(node, goal):
            return abs(node.row - goal.row) + abs(node.col - goal.col)

        def astar(grid, start, goal):
            if not (0 <= start[0] < len(grid) and 0 <= start[1] < len(grid[0]) and
                0 <= goal[0] < len(grid) and 0 <= goal[1] < len(grid[0])):
                    return []

            open_set = []
            closed_set = set()

            start_node = Node(start[0], start[1])
            goal_node = Node(goal[0], goal[1])

            heapq.heappush(open_set, start_node)

            while open_set:
                current_node = heapq.heappop(open_set)

                if current_node.row == goal_node.row and current_node.col == goal_node.col:
                    path = []
                    while current_node:
                        path.append((current_node.row, current_node.col))
                        current_node = current_node.parent
                    return path[::-1]

                closed_set.add((current_node.row, current_node.col))

                neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Adjust for diagonal movement if needed

                for n in neighbors:
                    new_row, new_col = current_node.row + n[0], current_node.col + n[1]

                    if (
                        0 <= new_row < len(grid) and
                        0 <= new_col < len(grid[0]) and
                        grid[new_row][new_col] != 1 and
                        (new_row, new_col) not in closed_set
                    ):
                        
                        neighbor = Node(new_row, new_col)
                        neighbor.g = current_node.g + 1
                        neighbor.h = heuristic(neighbor, goal_node)
                        neighbor.parent = current_node

                        if neighbor not in open_set:
                            heapq.heappush(open_set, neighbor)

                return []

    
    def match5(self, max_distance=2.0, verbose=False):
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
        self.add_passenger(passenger1)
        self.add_passenger(passenger2)
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
