import spacy
import pandas as pd
from spacy.tokens import DocBin
import functions  # custom functions file for preprocessing

'''
PRE-TRAINING
'''
spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")

# Importing train ant test data
input_data = pd.read_csv('Disinformation_Training_Data.csv')

col_name = "Disinformation"
input_data[col_name].value_counts()

n_sample = 50

input_data[col_name].value_counts()

random_data_col = functions.eq_division(input_data, n_sample=n_sample, cats_col_name=col_name)

train_col, test_col = functions.random_select(input_data=random_data_col, cats_column_name=col_name)
print("Training size:", len(train_col)), print("Test size:", len(test_col))

# Using the spacy.doc architecture for our data and saving it in a .spacy file for training
train_docs_col = functions.make_docs(nlp, train_col, cat_col_name=col_name, text_col_name='Text')
test_docs_col = functions.make_docs(nlp, test_col, cat_col_name=col_name, text_col_name='Text')

DocBin(docs=train_docs_col).to_disk('train.spacy')
DocBin(docs=test_docs_col).to_disk('test.spacy')
