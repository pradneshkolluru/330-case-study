from task1 import NotUber, passenger
import csv


with open('data/passengers.csv', newline='') as csvfile:
        
        test = NotUber()

        passengerreader = csv.reader(csvfile, delimiter=',', )

        passengerid = -1

        for row in passengerreader:

            if passengerid == -1:
                  
                  passengerid = passengerid + 1
                  continue

            test.add_passenger(passenger(passengerid, row[0], row[1], row[2]))
            passengerid = passengerid + 1