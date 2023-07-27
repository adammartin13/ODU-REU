import csv
import urllib.error
from urllib.request import urlopen
from urllib.parse import urlparse
import json
import pandas as pd


# function to add to JSON
def write_json(new_data, filename='brians_data.json'):
    with open(filename, 'r+', encoding='utf8') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        file_data["data"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


# check if link exists
def check_json(link, filename='brians_data.json'):
    with open(filename, encoding='utf8') as file:
        file_data = json.load(file)
        for object in file_data["data"]:
            if object["Link"] == link:
                return False

    return True


# get webpage title
def findTitle(html):
    title = html.split('<title>')[1].split('</title>')[0]
    return title


def main():
    with open('news_colombia_validation.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)

        viol_end_char = ['}', ')', ';', '=', '>', '_']
        viol_start_char = ["'", ';', '/', '%', '+', '(', '!', '{', '&', '`', '=']

        # These are websites that the scraper cannot operate on and are thustly ignored.
        # Recommend modifying for your use case. Current links are from largely Russian
        # disinfo sources.
        blacklist_websites = ['www.nytimes.com', 'en.news-front.info', 'tass.ru', 'news.mail.ru',
                              'www.defense.gov', 'www.independent.co.uk', 'www.forbes.com', 'www.gazeta.ru']

        # tracking index is necessary to remove csv lines that contain unicode URLs
        index = 0
        try:
            for row in reader:
                if not check_json(row[0]):  # check if item already exists
                    continue
                elif urlparse(row[0]).netloc in blacklist_websites:  # check if website is blacklisted
                    data = {
                        "Link": row[0],
                        "Return Code": "400",
                        "Publisher": urlparse(row[0]).netloc,
                        "Is Disinformation": row[1],
                        "Title": "",
                        "Text": ""
                    }
                    write_json(data)
                    continue

                data = {
                    "Link": row[0],
                    "Return Code": "",
                    "Publisher": urlparse(row[0]).netloc,
                    "Is Disinformation": row[1],
                    "Title": "",
                    "Text": ""
                }

                try:
                    resp = urlopen(row[0])
                    data["Return Code"] = resp.getcode()
                    html = resp.read().decode("utf8")
                    data["Title"] = findTitle(html)
                    html = html.split('<')
                    text = ''
                    for line in html:
                        line = line[line.find('>')+1:]
                        while '\n' in line:
                            line = line.replace('\n', '')  # Remove newline
                        while '\t' in line:
                            line = line.replace('\t', '')  # Remove tabs
                        while '  ' in line:
                            line = line.replace('  ', '')  # Remove space-tabs
                        try:
                            while line[0] == ' ':
                                line = line[1:]  # Remove leading spaces

                            # line[-2] also checks for lines with extending newline operators
                            # line.isnumeric() checks if line is a numeric value
                            if line[-2] not in viol_end_char and line[-1] not in viol_end_char and not line.isnumeric():
                                if line[0] not in viol_start_char:
                                    if 'http' not in line and line[0:3] != 'var' and \
                                            line[0:4] != 'icon' and line[0:6] != 'window' and \
                                            line[0:8] != 'document' and line[0:6] != 'jQuery':
                                        text += ' ' + line
                        except IndexError as e:
                            error = e
                    data["Text"] = text
                    print(data)
                    write_json(data)
                    resp.close()
                except urllib.error.HTTPError as e:
                    data["Return Code"] = 403
                    print(data)
                    write_json(data)
                except UnicodeDecodeError as e:
                    data["Return Code"] = 403
                    print(data)
                    write_json(data)
            index = index + 1
        except UnicodeDecodeError as e:
            data = pd.read_csv("news_colombia_validation.csv")
            data = data.drop(data.index[index])  # Remove bad URLs
            data.to_csv('news_colombia_validation.csv', index=False)
            main()  # Restart after csv edit

    print('Done.')
    quit()


main()
