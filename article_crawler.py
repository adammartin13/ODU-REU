import csv
import urllib.error
from urllib.request import urlopen
from urllib.parse import urlparse
import json

with open('Disinformation Training Data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        data = {
            "Link": row[0],
            "Return Code": "",
            "Publisher": urlparse(row[0]).netloc,
            "Is Disinformation": row[1],
            "Text": ""
        }
        try:
            resp = urlopen(row[0])
            data["Return Code"] = resp.getcode()
            print(data)
            # print(resp.read())
        except urllib.error.HTTPError as e:
            data["Return Code"] = 403
            print(data)

