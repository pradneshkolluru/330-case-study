import heapq
import datetime


class driver:
    def __init__(self, name, lat, long, time_available = 0):
        
        self.name = name
        self.loc = (lat, long)
        self.time_available = 0
    
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

        driver.time_available = datetime.datetime.now()
        heapq.heappush(self.available_drivers, driver)

    def add_passenger(self, passenger):
        heapq.heappush(self.unmatched_passengers, passenger)

    def match(self):

        if not self.available_drivers or not self.unmatched_passengers:
            return None

        driver = heapq.heappop(self.available_drivers)
        passenger = heapq.heappop(self.unmatched_passengers)
        dist = distance(driver.loc, passenger.sloc)

        return {
            'driver_id': driver.name,
            'passenger_id': passenger.name,
            'travel_time': dist,
        }


def find_time(start_location, end_location):
    return distance(start_location, end_location)

def distance(location1, location2):

    from math import sin, cos, sqrt, atan2, radians

    R = 6373.0

    lat1 = radians(location1[0])
    lon1 = radians(location1[1])
    lat2 = radians(location2[0])
    lon2 = radians(location2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance



if __name__ == "__main__":

    test = NotUber()

    test.add_new_driver(driver("billy", 40.66, -77.39))
    test.add_new_driver(driver("Nob", 40.66, -77.39))

    test.add_passenger(passenger("Sam","04/25/2014 00:00:00", 40.68, -77.38))

    print(test.match()) #Match


    test.add_passenger(passenger("Taylor","04/26/2014 00:00:00", 40.66, -77.40))

    print(test.match()) #Match

    test.add_passenger(passenger("Tom","04/25/2014 00:00:00", 40.66, -77.430))

    print(test.match()) #None

    test.add_passenger(passenger("Emma Stone","04/25/2014 00:00:00", 40.88, -77.42))

    print(test.match()) #None

    test.add_passenger(passenger("Dom","04/25/2014 00:00:00", 40.66, -79.40))

    print(test.match()) #None

    test.add_new_driver(driver("john", 40.88, -77.42))


    print(test.match()) #Match John to Emma
