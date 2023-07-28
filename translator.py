import csv
import json
import re
from deep_translator import GoogleTranslator


# read JSON file
def read_json(link, filename='article_data.json'):
    with open(filename, encoding='utf8') as file:
        file_data = json.load(file)
        for object in file_data["data"]:
            if object["Link"] == link:
                return object["Text"]


# function to add to JSON
def write_json(new_data, filename='translated_text.json'):
    with open(filename, 'r+', encoding='utf8') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        file_data["data"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


# check if link exists
def check_json(link, filename='translated_text.json'):
    with open(filename, encoding='utf8') as file:
        file_data = json.load(file)
        for object in file_data["data"]:
            if object["Link"] == link:
                return False

    return True


# Clean article text
def clean_text(text):
    bad_chars = [',', '!', '?', ';', ':', '.']
    for i in bad_chars:  # Remove special characters
        text = text.replace(i, '')
    return text


with open('Disinformation_Training_Data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        if not check_json(row[0]):
            continue

        to_translate = re.split(r'[,!?;:.]', read_json(row[0]))
        iterator = 0
        translated = ''
        for word in to_translate:
            try:
                translated += GoogleTranslator(source='auto', target='en').translate(word) + ' '
            except TypeError:
                translated += word + ' '

        translated = clean_text(translated)

        data = {
            "Link": row[0],
            "Text": read_json(row[0]),
            "Text-Translated": translated
        }

        write_json(data)
        print(read_json(row[0]))
        print(translated)

