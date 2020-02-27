import requests
import json


class TestClass():
    def test_one(self):
        url = "http://127.0.0.1:5000/getjson"

        r = requests.get(url)

        print(r.status_code)
        print(r.text)
        print(type(r.text))

        print(json.loads(r.text))
        print(type(json.loads(r.text)))

        for row in json.loads(r.text):
            print(row)

