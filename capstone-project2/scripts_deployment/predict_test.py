import requests
import json

url = 'http://localhost:9696/predict'
json_appr = {
  "steps": 12
}

response = requests.post(url, json=json_appr).json()
json_formatted_str = json.dumps(response, indent=4)
print('Value to disburse %s' % json_formatted_str)