from uberAlgos import NotUber, passenger, driver
import csv
from helperFuncs import closestNodesDijkstra, genAdj
import datetime
import timeit

test = NotUber()

# addPassengers
with open('data/passengers.csv', newline='') as csvfile:
        

        passengerreader = csv.reader(csvfile, delimiter=',', )

        passengerid = -1

        for row in passengerreader:

            if passengerid == -1:
                  
                  passengerid = passengerid + 1
                  continue
            
            # if passengerid == 4:
            #       break

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

profit_list = []
passengers_waiting_list = []

def execModel(verbose = True):

      totalnumPassengers = len(test.unmatched_passengers)

      while (len(test.unmatched_passengers) > 0 and len(test.available_drivers) > 0):
            
            match = test.match1()

            if verbose:
                  #print(match)

                  progress = round(((totalnumPassengers - len(test.unmatched_passengers)) * 100) / totalnumPassengers, 2)


                  print(f"{progress}% Completed")

                  # if progress > 1.0:
                  #       break
            
            t1 = closestNodesDijkstra(match['passenger_obj'].sloc, match['driver_obj'].loc, match['passenger_obj'].startTime)
            t2 = closestNodesDijkstra(match['passenger_obj'].sloc, match['passenger_obj'].dloc, match['passenger_obj'].startTime)
            t3 = 0
            if not (match['available_immediately']):
                  
                  #print(datetime.datetime.strftime(match['driver_obj'].time_available, "%m/%d/%Y %H:%M:%S"))
                  #print(datetime.datetime.strftime(match['passenger_obj'].startTime, "%m/%d/%Y %H:%M:%S"))

                  time_difference = match['driver_obj'].time_available - match['passenger_obj'].startTime

                  #print(time_difference)
                  t3 = time_difference.total_seconds() / 3600
                  #print(t3)
                  #print(t3)
            recycled_driver = match['driver_obj']
            recycled_driver.time_available = recycled_driver.time_available + datetime.timedelta(hours=t1) + datetime.timedelta(hours=t2) + datetime.timedelta(hours=t3)
            recycled_driver.loc = match['passenger_obj'].dloc
        
            profit = (t2*60) - (t1*60)
            profit_list.append(profit)

            passengers_waiting_list.append(t1*60)

            #print(recycled_driver.time_available)
            test.add_new_driver(recycled_driver)


if __name__ == "__main__":

      execution_time = timeit.timeit(execModel, number=1)
      print("Execution time:", execution_time, "seconds")

      avg_profit = sum(profit_list)/float(len(profit_list))
      print("Average profit: ", avg_profit)
      sum_profit = sum(profit_list)
      print("Profit sum: ", sum_profit)


      avg_time_waiting = sum(passengers_waiting_list)/float(len(passengers_waiting_list))
      print("Average passenger waittime: ", avg_time_waiting)

      sum_time_waiting = sum(passengers_waiting_list)
      print("Passenger waittime sum: ", sum_time_waiting)