import heapq

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

        travel_time = find_time(driver.location, passenger.pickup_location)
        driver.location = passenger.dropoff_location

        return {
            'driver_id': driver.id,
            'passenger_id': passenger.id,
            'travel_time': travel_time
        }

def find_time(start_location, end_location):
    return distance(start_location, end_location)

def distance(location1, location2):
    return 1


result = NotUber().match()
print(result)
