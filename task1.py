import heapq
import geopy.distance


class driver:
    def __init__(self, name, lat, long):
        
        self.name = name
        self.loc = (lat, long)

class passenger:
    def __init__(self, name, slat, slong, dlat = 0, dlong = 0):
        
        self.name = name
        self.sloc = (slat, slong)
        self.dloc = (dlat, dlong)



class NotUber:
    def __init__(self):
        self.available_drivers = []
        self.unmatched_passengers = []

    def add_driver(self, driver):
        heapq.heappush(self.available_drivers, driver)

    def add_passenger(self, passenger):
        self.unmatched_passengers.append(passenger)

    def match(self):
        if not self.available_drivers or not self.unmatched_passengers:
            return None

        driver = heapq.heappop(self.available_drivers)
        passenger = self.unmatched_passengers.pop(0)

        travel_time = find_time(driver.loc, passenger.sloc)
        #driver.location = passenger.dropoff_location

        return {
            'driver_id': driver.name,
            'passenger_id': passenger.name,
            'travel_time': travel_time
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

    test.add_driver(driver("billy", 40.66, -77.39))

    test.add_passenger(passenger("Sam", 40.68, -77.38))

    #print(test.match())

    test.add_passenger(passenger("Tom", 40.66, -77.40))

    #print(test.match())

    test.add_driver(driver("john", 40.88, -77.42))

    #print(test.match())