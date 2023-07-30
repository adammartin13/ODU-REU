from unicodedata import category
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import metrics
import re


def eq_division(data, categories=None, n_sample=None, cats_col_name='frustration'):
    """
        Divide a dataframe into equal number of samples for each category.

        Parameters
            data:           The dataframe to be split.
            categories:     The list of the categories to be used.
            n_sample:       The number of observations per category.

        Returns
            train, test:    The train and test dataframes.
    """
    if categories:
        data = data[data[cats_col_name].isin(categories)]
    divided_data = pd.DataFrame()

    for cat in data[cats_col_name].unique():
        sub_data = data[data[cats_col_name] == cat]
        if n_sample:
            sub_data = sub_data.sample(n_sample)
        divided_data = pd.concat([divided_data, sub_data])

    return divided_data


def random_select(input_data=pd.DataFrame, cats_column_name='frustration', test_size=0.3, random_state=0):
    """
        Selects randomly the test and train set from a given dataframe.

        Parameters
            input_data:         The dataframe to be split.
            cats_column_name:   The name of the column containing the categories.
            test_size:          The proportion of the test set (0 to 1).
            random_state:       The random state (seed) to be used.

        Returns
            train, test:    The train and test dataframes.
    """
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()
    for frust_type in input_data[cats_column_name].unique():
        sub_data = input_data[input_data[cats_column_name] == frust_type]
        train, test = train_test_split(sub_data, test_size=test_size, random_state=random_state)
        train_data = pd.concat([train_data, train])
        test_data = pd.concat([test_data, test])
    return (train_data, test_data)


def make_docs(model, data, text_col_name='paragraph', cat_col_name='frustration'):
    """
        Generate a .spacy file from a dataframe to train a model.

        Parameters
            data:               The dataframe with texts and categories.
            model:              The model pipeline to generate the output in its specific format.
            text_col_name:      The name of the column containing the texts.
            cat_col_name:       The name of the column containing the categories.

        Returns
            docs:   The list of documents for training the model.
    """
    categories = data[cat_col_name].unique()
    data = list(data[[text_col_name, cat_col_name]].apply(tuple, axis=1))
    docs = []
    for doc, label in model.pipe(data, as_tuples=True):
        for category in categories:
            if label == category:
                doc.cats[category] = 1
            else:
                doc.cats[category] = 0

        docs.append(doc)
    return (docs)


def predict_spacy(dataframe, model, text_col_name='paragraph'):
    """
        Predicts the categories from a dataframe of texts using a trained SpaCy model.

        Parameters
            dataframe:      The dataframe with texts.
            model:          The pre-trained or trained model to make the predictions.
            text_col_name:      The name of the column containing the texts.

        Returns
            dataframe:      The dataframe with the predicted categories (in the 'predicted' column).
    """
    y_pred = []
    for text in list(dataframe[text_col_name]):
        max_val = max(model(text).cats.values())
        for key in model(text).cats.keys():
            if model(text).cats[key] == max_val:
                y_pred.append(key)
    dataframe['predicted'] = y_pred
    return (dataframe)


def predict_cat(string, model):
    """
        Predicts the category from a string using the trained model.

        Parameters
            str:      The string to be predicted.

        Returns
            cat:      The predicted category.
    """
    for key in model(string).cats.keys():
        if model(string).cats[key] == max(model(string).cats.values()):
            cat = key
    return (cat)


def conf_matrix(dataframe, cat_col_name='frustration', predicted_col_name='predicted'):
    """
        Calculates the confusion matrix from a dataframe with predicted and actual categories.

        Parameters
            dataframe:      The dataframe with predicted and actual categories.
            categories:     The list of the categories to be used.
            cat_col_name:   The name of the column containing the categories.

        Returns
            matrix:         The confusion matrix.
    """
    categories = dataframe[cat_col_name].unique()
    n_cats = len(categories)
    cm = metrics.confusion_matrix(dataframe[cat_col_name], dataframe[predicted_col_name])
    acc = metrics.accuracy_score(dataframe[cat_col_name], dataframe[predicted_col_name])
    plt.clf()
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.suptitle('Confusion Matrix - ')
    plt.title('Accuracy: ' + str(round(acc, 3)))
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    tick_marks = np.arange(n_cats)
    plt.xticks(tick_marks, categories, rotation=45)
    plt.yticks(tick_marks, categories)
    for i in range(n_cats):
        for j in range(n_cats):
            plt.text(i, j, str(cm[i][j]))
    plt.show()


def tweet_text_clean(text):
    """
        Cleans the text of a tweet deleting unnecesary symbols, accents and emojis

        Parameters
            text:   Tweet text string

            Returns
            text:   Cleaned tweet text string

    """
    # 1. Links
    text = re.sub('http[s]?://\S+', '', text)
    text = re.sub('http[s]?', '', text)
    # 2. html entities
    text = re.sub('&.{1,5};', '', text)

    # 3. RT @username
    text = re.sub('RT.@{1}.+?:', '', text)

    # 4. emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", re.UNICODE)

    text = emoji_pattern.sub('', text)
    # 5. symbols
    text = re.sub(r'[^(\w,. )]', '', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'[\,]{2,}', ',', text)
    text = text.strip()
    return (text)
