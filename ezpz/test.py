import requests

url= "http://localhost:3000/data"
resp = requests.get(url)
data = resp.json()
print(data)