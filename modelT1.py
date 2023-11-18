from task1 import NotUber, passenger, driver
import csv
from testDijkstra import closestNodesDijkstra
import datetime

test = NotUber()

# addPassengers
with open('/Users/emmachun/Downloads/data/passengers.csv', newline='') as csvfile:
        

        passengerreader = csv.reader(csvfile, delimiter=',', )

        passengerid = -1

        for row in passengerreader:

            if passengerid == -1:
                  
                  passengerid = passengerid + 1
                  continue

            for i in range(1, len(row)):
                    row[i] = float(row[i])

            test.add_passenger(passenger(passengerid, row[0], row[1], row[2], row[3], row[4]))
            passengerid = passengerid + 1

# addDrivers
with open('/Users/emmachun/Downloads/data/drivers.csv', newline='') as csvfile:

        driverreader = csv.reader(csvfile, delimiter=',', )

        driverid = -1

        for row in driverreader:

            if driverid == -1:
                  
                  driverid = driverid + 1
                  continue

            for i in range(1, len(row)):
                    row[i] = float(row[i])

            test.add_new_driver(driver(driverid, row[1], row[2], row[0]))
            driverid = driverid + 1



while (len(test.unmatched_passengers) > 0 and len(test.available_drivers) > 0):
      
      match = test.match1()
      print(match)
      t1 = float(closestNodesDijkstra(match['passenger_obj'].sloc, match['driver_obj'].loc, match['passenger_obj'].startTime))
      t2 = float(closestNodesDijkstra(match['passenger_obj'].sloc, match['passenger_obj'].dloc, match['passenger_obj'].startTime))
      print(t1)
      print(t2)
      #print(type(t1))
      recycled_driver = match['driver_obj']
      recycled_driver.time_available = recycled_driver.time_available + datetime.timedelta(hours=t1) + datetime.timedelta(hours=t2)
      test.add_new_driver(recycled_driver)