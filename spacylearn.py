import spacy
from spacy.tokens import Doc, Span

nlp = spacy.blank('en')
'''
doc = nlp("Hello, World!")


for token in doc:
    print(token.text)  # Prints each token

print(doc[2])  # Prints third token: World
'''
'''
doc = nlp("I want 5 dollars.")
print([token.text for token in doc])  # Prints tokens
print([token.is_alpha for token in doc])  # Prints alphabetical token booleans
print([token.like_num for token in doc])  # Prints numeric token booleans
'''
'''
words = ["Hello", "World", "!"]
spaces = [True, False, False]
doc = Doc(nlp.vocab, words=words, spaces=spaces)  # Create a doc object from tokens
print([token.text for token in doc])
span = Span(doc, 0, 2)
span_with_label = Span(doc, 0, 2, label="Greeting")  # Create a span object from the doc
doc.ents = [span_with_label]
print(doc.ents)
'''
nlp = spacy.load("en_core_web_lg")
doc1 = nlp("Ukrainians are Nazis")
doc2 = nlp("Ukrainians are not Nazis")
print(doc1.similarity(doc2))
