import requests
import json

url = 'http://0.0.0.0:1717'
#port = 1717
headers = {"Content-Type":"application/json"}
data ={
    "door_position":"0"
}

response = requests.post(url,headers = headers, data = json.dumps(data))
print(response.text)