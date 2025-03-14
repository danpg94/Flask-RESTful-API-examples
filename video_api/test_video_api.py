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
for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
input()
# Deleting a specific video metadata (Testing DELETE)
response = requests.delete(BASE + "video/0")
print(response)
input()
# Requesting a specific video metadata (Testing GET)
response = requests.get(BASE + "video/2")
print(response.json())