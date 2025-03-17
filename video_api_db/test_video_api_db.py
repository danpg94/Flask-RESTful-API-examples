#Simple CRUD test for main.py api

import requests

BASE = "http://0.0.0.0:5000/"

# Example data to be added to server
data = [{"likes": 564, "name": "REST API Tutorial", "views": 3487},
        {"likes": 2341, "name": "Insane SM64 speedrun", "views": 7865},
        {"likes": 10675, "name": "What happened to Carbon?", "views": 65234},
        {"likes": 78, "name": "Smells like teen spirit cover", "views": 1932},
        {"likes": 26, "name": "blog: my day out", "views": 545}]

# Adding data to server (Testing PUT)
print(f"Adding video metadata to db:")
for i in range(len(data)):
    print(f"id: {i} name:{data[i]['name']} likes: {data[i]['likes']} views: {data[i]['views']}")
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(f"Response: {response}")
input("Press enter to continue")

# Requesting a specific video metadata entry (Testing GET)
print(f"Requesting video metadata from db:")
response = requests.get(BASE + "video/2")
print(response.json())
input("Press enter to continue")

# Editing a specific video metadata entry (Testing PATCH)
print(f"Editing video metadata from db:")
response = requests.patch(BASE + "video/2", {"views": 100, "likes": 100})
print(response.json())
input("Press enter to continue")

# Deleting a specific video metadata (Testing DELETE)
print(f"Deleting video metadata from db:")
for i in range(len(data)):
    response = requests.delete(BASE + "video/" + str(i))
    print(response)
input("Press enter to continue")