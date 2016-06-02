import json
from pdftojsonl import process_pdfs
from txtprocess import KeySelect, StripTransform, CosineSim
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

'''
'''

def similarity(target, candidate):

    pipe = Pipeline([
        ('bykey', KeySelect()),
        ('clean', StripTransform()),
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('cosine', CosineSim())
    ])

    return 1 - pipe.fit(target, None).predict(candidate)






