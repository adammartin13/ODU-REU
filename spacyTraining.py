import spacy
import pandas as pd
import functions
import time
import torch

'''
MODEL TRAINING
'''

spacy.prefer_gpu(0)

# Change this to the name of the column in your dataset you want to train on
col_name = "Disinformation"

# !python -m spacy init fill-config spacy_files/en_lg_config2.cfg spacy_files/en_lg_config2.cfg


# Import model, and test file for evaluation (accuracy + confusion matrix)
nlp = spacy.load("./"+colname+'/'+spacy_model+'/model-last')
test = pd.read_excel("./"+colname+'/test.xlsx')
test[colname] = test[colname].astype(str) #convert to string

# Predict on test set. Ans save to excel with predictions
test_with_predictions = functions.predict_spacy(test,nlp, text_col_name='text')
test_with_predictions.to_excel("./"+colname+'/test_with_preds.xlsx', index = False)

functions.conf_matrix(test_with_preds, cat_col_name=colname)
