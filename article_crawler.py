import csv
import urllib.error

import requests
from urllib.request import urlopen
import json

with open('Disinformation Training Data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        # resp = requests.get(row[0])
        data = {
            "Link": row[0],
            "Return Code": "",
            "Publisher": "",
            "Is Disinformation": row[1],
            "Text": ""
        }
        # print(data)
        try:
            resp = urlopen(row[0])
            print(resp.getcode())
        except urllib.error.HTTPError as e:
            print(e)

