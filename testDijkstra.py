import csv
import sys
import heapq

adjacency = {}

class path:
    def __init__(self, end_id, length, weekday, weekend):
        
        self.id = end_id
        self.length = length
        self.weekdaySpeeds = weekday #list
        self.weekendSpeeds = weekend #list
        self.weekdayTimes = self.calcTimes("weekday")
        self.weekendTimes = self.calcTimes("weekend")

    def calcTimes(self, dayType):

        retWeekend = []
        retWeekday = []

        for i in range(len(self.weekdaySpeeds)):

            retWeekday.append(self.length / self.weekdaySpeeds[i])
            retWeekend.append(self.length / self.weekendSpeeds[i])

        if dayType == 'weekend':
            return retWeekend
        else:
            return retWeekday
        
    def getTimeTraversal(date):


        if date.weekday() in range(0, 5):

            dayType = "weekday"

        else:
            dayType = "weekend"

        hour = date.hour

        return (dayType, hour)




def genAdj():
    with open('data/edges.csv', newline='') as csvfile:

            edgeReader = csv.reader(csvfile, delimiter=',', )

            edgeId = -1

            for row in edgeReader:


                if edgeId == -1:
                    
                    edgeId = edgeId + 1
                    continue
                
                for i in range(len(row)):
                    row[i] = float(row[i])
                
                newPath = path(row[1], row[2], row[3:27], row[27:])
                
                
                if row[0] not in adjacency.keys():
                    
                    adjacency[row[0]] = []
                
                adjacency[row[0]].append(newPath)

                edgeId = edgeId + 1


def dijkstra(graph, start, end):
    #start by setting everything to infinity like usual
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0 # starting node distance to itself is 0

    # priority queue to keep track of what node to visit next
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

    # if distance at node is shorter than current distance, ignore
        if current_distance > distances[current_node]:
            continue

    # check neighbors
        for neighbor_path in graph.get(current_node, []):
            total_distance = current_distance + neighbor_path.weekdayTimes[0]

            # Check if the new distance is shorter than the known distance to the neighbor.
            if total_distance < distances[neighbor_path.id]:
                distances[neighbor_path.id] = total_distance
                heapq.heappush(priority_queue, (total_distance, neighbor_path.id))

    # Return the shortest distance to the end node.
    return distances[end]

# # Example usage
# source_node = 12345678 # Replace with your actual source node ID
# end_node = 39076461 # Replace with your actual end node ID

# shortest_distance = dijkstra(adjacency, source_node, end_node)

# print(f"Shortest distance from {source_node} to {end_node}: {shortest_distance}")

def main():
    #adjacency = {1: [path(2, 5, [40], [40]), path(3, 30, [40], [40])], 2: [path(1, 5, [50], [50]), path(3, 5, [50], [50])], 3:[path(2, 5, [50] ,[50]), path(1, 30, [15], [15])]}

    # genAdj()
    # shortest_distance = dijkstra(adjacency, 39076461, 42847609)
    
    
    adjacency = {1: [path(2, 5, [40], [40]), path(3, 5, [100], [40])], 2: [path(1, 5, [100], [50]), path(3, 5, [40], [50])], 3:[path(2, 5, [50], [50]), path(1, 30, [15], [15])]}

    shortest_distance = dijkstra(adjacency, 1, 3)

    print(shortest_distance)


if __name__ == "__main__":
    main()