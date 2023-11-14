import csv

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

print(adjacency[39076461])
for i in adjacency[39076461]:
     
    print(i.id, i.length, i.weekdaySpeeds)