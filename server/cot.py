import requests
import json

class cot_api:
    def __init__(self, token):
        self.token = token

    def get_data(self, key):
        print("getting data...")
        payload = {"Key": key, "Value": 0, "Token": self.token}
        response=requests.get('https://circusofthings.com/ReadValue',params=payload)
        return json.loads(response.content) # Returns response from server as a loaded json object

    def write_data(self, key, value):
        print("writing data...")
        payload = {"Key": key, "Value": value, "Token": self.token}
        response=requests.put('https://circusofthings.com/WriteValue',
				data=json.dumps(payload),headers={'Content-Type':'application/json'})
        return json.loads(response.content) # Returns response from server as a loaded json object