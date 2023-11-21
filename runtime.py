from uberAlgos import NotUber, passenger, driver
import csv
from helperFuncs import closestNodesDijkstra, genAdj
import datetime
import timeit

test = NotUber()

# addPassengers

def create_test_data(n, m):

    with open('data/passengers.csv', newline='') as csvfile:
            

            passengerreader = csv.reader(csvfile, delimiter=',', )

            passengerid = -1

            for row in passengerreader:

                if passengerid == -1:
                    
                    passengerid = passengerid + 1
                    continue
                
                if passengerid == n:
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
                
                if driverid == m:
                      break

                for i in range(1, len(row)):
                        row[i] = float(row[i])

                test.add_new_driver(driver(driverid, row[1], row[2], row[0]))
            driverid = driverid + 1



num_drivers = 10
num_passengers = 10

create_test_data(num_drivers, num_passengers)

def measureRuntime():
      
      test.match1()


exec_time = timeit.timeit(measureRuntime, number=1000)
print(f"Execution time of match1() for {num_drivers} drivers and {num_passengers} passengers: {exec_time} seconds")

