import spacy
import pandas as pd
import functions
import time
import torch

'''
MODEL TESTING
'''

spacy.prefer_gpu(0)

# Change this to the name of the column in your dataset you want to train on
col_name = "Disinformation"

# Import model, and test file for evaluation (accuracy + confusion matrix)
# spacy.cli.download("en_core_web_lg")  # Uncomment if needing to re-download the model
nlp = spacy.load("en_core_web_lg")
test = pd.read_csv('test.csv')

# Predict on test set. And save to excel with predictions
test_with_predictions = functions.predict_spacy(test, nlp, text_col_name='Text')
test_with_predictions.to_csv('test_with_preds.csv', index=False)
