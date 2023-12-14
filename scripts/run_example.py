import requests
import json
import sys

url = "http://localhost:5000/configure_all"
example = sys.argv[1]
f = None

if example == "baby-monitor":
    f = open("./models/bm_model.json")
elif example == "smart-home":
    f = open("./models/sh_model.json")
elif example == "autonomous-vehicle":
    f = open("./models/av_model.json")
else:
    print("Example not recognized")
    sys.exit(1)

payload = json.dumps(json.load(f))
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
