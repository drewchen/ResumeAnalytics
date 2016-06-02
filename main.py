import json
from pdftojsonl import process_pdfs
from txtprocess import KeySelect, StripTransform, CosineSim
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

'''
'''

if __name__ == '__main__':

    pipe = Pipeline([
        ('bykey', KeySelect()),
        ('clean', StripTransform()),
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('cosine', CosineSim())
    ])

    with open('out.jsonl') as f:
        data = [json.loads(line) for line in f]
    d = pipe.fit(data, None)

    print(d.predict(data))
