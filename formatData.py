import pandas as pd

translated_data = pd.read_json('translated_text.json')
original_data = pd.read_csv('Disinformation_Training_Data.csv')

for x in range(original_data["Link"].size):
    for article in translated_data["data"]:
        if original_data.loc[x, 'Link'] == article["Link"]:
            original_data.loc[x, 'Text'] = article["Text-Translated"]
            original_data.to_csv("Disinformation_Training_Data.csv", index=False)
