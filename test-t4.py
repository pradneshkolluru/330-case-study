import json

def sort_coordinates():
    with open("data/node_data.json", 'r') as file:
        data = json.load(file)

    # sorts the data based on latitude first and then longitude
    sorted_data = sorted(data.items(), key=lambda item: (item[1]['lat'], item[1]['lon']))

    # Create a new dictionary from the sorted data
    sorted_dict = dict(sorted_data)

    return sorted_dict

sorted_coordinates_dict = sort_coordinates()


for i, (key, value) in enumerate(sorted_coordinates_dict.items()):
    if i < 5:
        print(f"{key}: {value}")
    else:
        break

print("break")

total_elements = len(sorted_coordinates_dict)
for i, (key, value) in enumerate(sorted_coordinates_dict.items()):
    if i >= (total_elements - 5):
        print(f"{key}: {value}")

#print(sorted_coordinates_dict)