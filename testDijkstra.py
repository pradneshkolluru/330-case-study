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
    # Initialize distances with infinity for all nodes except the start node.
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0 # The distance from the start node to itself is 0.

    # Use a priority queue (min heap) to keep track of the next node to visit.
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

    # If the current node has already been visited with a shorter distance, skip it.
        if current_distance > distances[current_node]:
            continue

    # Check neighbors of the current node.
    for neighbor_path in graph.get(current_node, []):
        total_distance = current_distance + neighbor_path.length

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
    shortest_distance = dijkstra(adjacency, 39076461, 42847609)
    
    print(shortest_distance)

if __name__ == "__main__":
    main()
