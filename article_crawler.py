import csv
import requests
import json

with open('Disinformation Training Data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        print(row[0])
        resp = requests.get(row[0])
        print(resp.status_code)
        print(resp.text)
