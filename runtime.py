from uberAlgos import NotUber, passenger, driver
import csv
from helperFuncs import closestNodesDijkstra, genAdj
import datetime
import timeit
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

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



testValues = [0, 2, 5, 10, 20, 40, 80, 160, 320, 500]

driverct = np.zeros(len(testValues))
passengerct = np.zeros(len(testValues))
runtime = np.zeros(len(testValues))



for i in range(0, len(testValues)):

    num_drivers = num_passengers = testValues[i]

    create_test_data(num_drivers, num_passengers)

    driverct[i] = testValues[i]
    passengerct[i] = testValues[i]



    def measureRuntime():
        
        test.match3_efficient()


    exec_time = timeit.timeit(measureRuntime, number=1)

    runtime[i] = exec_time

    print(f"Execution time of match for {num_drivers} drivers and {num_passengers} passengers: {exec_time} seconds")


totalct = driverct + passengerct

sns.scatterplot(x = totalct, y = runtime)

# Set plot labels and title
plt.xlabel('Driver Count + Passenger Count')
plt.ylabel('Runtime')
plt.title('Driver Count vs Runtime')
plt.grid(True)

# Show the plot
plt.savefig("runtimeGraphs/task3_efficient.png")