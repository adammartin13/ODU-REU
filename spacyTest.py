import pandas as pd
import string
import spacy
import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn import metrics
from nltk.corpus import stopwords
from spacy.tokenizer import Tokenizer

#  nltk.download('stopwords')  # Uncomment if updating nltk
stopwords = stopwords.words('english')
df = pd.read_csv('Disinformation_Training_Data.csv')
df.head()

train, test = train_test_split(df, test_size=0.30, random_state=50)
print('Research text sample:', train['Text'].iloc[0])
print('Training Data Shape:', train.shape)
print('Testing Data Shape:', test.shape)

nlp = spacy.load("en_core_web_lg")
punctuations = string.punctuation


def cleanup_text(docs, logging=False):
    texts = []
    counter = 1
    for doc in docs:
        if counter % 1000 == 0 and logging:
            print("Processed %d out of %d documents." % (counter, len(docs)))
        counter += 1
        doc = nlp(doc, disable=['parser', 'ner'])
        tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
        tokens = [tok for tok in tokens if tok not in stopwords and tok not in punctuations]
        tokens = ' '.join(tokens)
        texts.append(tokens)
    return pd.Series(texts)


#  Most common words used
DISINFO_text = [text for text in train[train['Disinformation'] == 1]['Text']]
PROINFO_text = [text for text in train[train['Disinformation'] == 0]['Text']]

DISINFO_clean = cleanup_text(DISINFO_text)
DISINFO_clean = ' '.join(DISINFO_clean).split()
PROINFO_clean = cleanup_text(PROINFO_text)
PROINFO_clean = ' '.join(PROINFO_clean).split()

DISINFO_counts = Counter(DISINFO_clean)
PROINFO_counts = Counter(PROINFO_clean)

DISINFO_common_words = [word[0] for word in DISINFO_counts.most_common(20)]
DISINFO_common_counts = [word[1] for word in DISINFO_counts.most_common(20)]

# Most common words used in Russian Disinformation
fig = plt.figure(figsize=(18, 6))
sns.barplot(x=DISINFO_common_words, y=DISINFO_common_counts)
plt.title('Most Common Words used in Russian Disinformation')
plt.show()

PROINFO_common_words = [word[0] for word in PROINFO_counts.most_common(20)]
PROINFO_common_counts = [word[1] for word in PROINFO_counts.most_common(20)]

# Most common words used in Pro-Information Sources
fig = plt.figure(figsize=(18,6))
sns.barplot(x=PROINFO_common_words, y=PROINFO_common_counts)
plt.title('Most Common Words used in Pro-Information Sources')
plt.show()


def printNMostInformative(vectorizer, clf, N):
    feature_names = vectorizer.get_feature_names_out()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    topClass1 = coefs_with_fns[:N]
    topClass2 = coefs_with_fns[:-(N + 1):-1]
    print("Class 1 best: ")
    for feat in topClass1:
        print(feat)
    print("Class 2 best: ")
    for feat in topClass2:
        print(feat)

tokenizer = nlp.tokenizer
vectorizer = CountVectorizer(tokenizer=tokenizer, ngram_range=(1, 1))

clf = LinearSVC()

class CleanTextTransformer(TransformerMixin):
    def transform(self, X, **transform_params):
        return [cleanText(text) for text in X]
    def fit(self, X, y=None, **fit_params):
        return self

def cleanText(text):
    text = text.strip().replace("\n", " ").replace("\r", " ")
    text = text.lower()
    return text

pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer), ('clf', clf)])  # data
train1 = train['Text'].tolist()
labelsTrain1 = train['Disinformation'].tolist()
test1 = test['Text'].tolist()
labelsTest1 = test['Disinformation'].tolist()
# train
pipe.fit(train1, labelsTrain1)# test
preds = pipe.predict(test1)
print("accuracy:", accuracy_score(labelsTest1, preds))
print("Top 10 features used to predict: ")

printNMostInformative(vectorizer, clf, 10)
pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer)])
transform = pipe.fit_transform(train1, labelsTrain1)
vocab = vectorizer.get_feature_names_out()
for i in range(len(train1)):
    s = ""
    indexIntoVocab = transform.indices[transform.indptr[i]:transform.indptr[i+1]]
    numOccurences = transform.data[transform.indptr[i]:transform.indptr[i+1]]
    for idx, num in zip(indexIntoVocab, numOccurences):
        s += str((vocab[idx], num))

