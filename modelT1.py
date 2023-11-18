from uberAlgos import NotUber, passenger, driver
import csv
from helperFuncs import closestNodesDijkstra, genAdj
import datetime

test = NotUber()

# addPassengers
with open('data/passengers.csv', newline='') as csvfile:
        

        passengerreader = csv.reader(csvfile, delimiter=',', )

        passengerid = -1

        for row in passengerreader:

            if passengerid == -1:
                  
                  passengerid = passengerid + 1
                  continue
            
            if passengerid == 4:
                  break

            for i in range(1, len(row)):
                    row[i] = float(row[i])

            test.add_passenger(passenger(passengerid, row[0], row[1], row[2], row[3], row[4]))
            passengerid = passengerid + 1

# addDrivers
with open('data/drivers.csv', newline='') as csvfile:

        driverreader = csv.reader(csvfile, delimiter=',', )

        driverid = -1

        for row in driverreader:

            if driverid == -1:
                  
                  driverid = driverid + 1
                  continue
            
        #     if driverid == 2:
        #           break

            for i in range(1, len(row)):
                    row[i] = float(row[i])

            test.add_new_driver(driver(driverid, row[1], row[2], row[0]))
            driverid = driverid + 1

while (len(test.unmatched_passengers) > 0 and len(test.available_drivers) > 0):
      
      match = test.match1()
      print(match)
      
      t1 = closestNodesDijkstra(match['passenger_obj'].sloc, match['driver_obj'].loc, match['passenger_obj'].startTime)
      t2 = closestNodesDijkstra(match['passenger_obj'].sloc, match['passenger_obj'].dloc, match['passenger_obj'].startTime)
      t3 = 0
      if not (match['available_immediately']):
            
            print(datetime.datetime.strftime(match['driver_obj'].time_available, "%m/%d/%Y %H:%M:%S"))
            print(datetime.datetime.strftime(match['passenger_obj'].startTime, "%m/%d/%Y %H:%M:%S"))

            time_difference = match['driver_obj'].time_available - match['passenger_obj'].startTime

            print(time_difference)
            t3 = time_difference.total_seconds() / 3600
            print(t3)
            print(t3)
      recycled_driver = match['driver_obj']
      recycled_driver.time_available = recycled_driver.time_available + datetime.timedelta(hours=t1) + datetime.timedelta(hours=t2) + datetime.timedelta(hours=t3)
      recycled_driver.loc = match['passenger_obj'].dloc

      print(recycled_driver.time_available)
      test.add_new_driver(recycled_driver)