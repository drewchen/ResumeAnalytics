import re
import string
import json
import sklearn as sk
import numpy as np
from nltk.corpus import stopwords
from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator
from sklearn.metrics.pairwise import pairwise_distances


PUNCT = re.compile('[%s]' % re.escape(string.punctuation))
STOPS = set(stopwords.words('english'))


def _strip_punct(content):
    ''' remove all punctuation
    '''
    return PUNCT.sub('', content)


def _strip_numbers(content):
    ''' remove all digits
    '''
    return ''.join([i for i in content if not i.isdigit()])


def _strip_stops(content):
    return ' '.join([x for x in content.split()
                     if x not in STOPS])



class KeySelect(TransformerMixin):
    ''' select key from dictionary
    '''
    def __init__(self, key='content'):
        self.key = key

    def transform(self, X, **transform_params):
        return [x[self.key] for x in X]

    def fit(self, X, y=None, **fit_params):
        return self


class FileIterKeySelect(TransformerMixin):
    ''' select key from dictionary
    '''
    def __init__(self, xkey='content', ykey='label'):
        self.xkey = xkey
        self.ykey = ykey

    def _json_load(self, line):
        return json.loads(line)

    def _select_keys(self, element):
        return element[self.xkey], element[self.ykey]

    def transform(self, f, **transform_params):
        x, y = zip(*[self._select_keys(self._json_load(line)) for line in f])
        yield x, y

    def fit(self, X, y=None, **fit_params):
        return self


class StripTransform(TransformerMixin):
    ''' transform raw content to only word chars
    '''
    def transform(self, X, **transform_params):
        return [_strip_stops(_strip_numbers(_strip_punct(x)))
                 for x in X]

    def fit(self, X, y=None, **fit_params):
        return self


class CosineSim(BaseEstimator):
    ''' store vector of target, predict by calculating cosine distance
    '''
    def transform(self, X, **transform_params):
        return self

    def fit(self, X, y=None, **fit_params):
        indices = np.array([e for e in y if e == 2]).nonzero()[0]
        self.X = X[indices, :]

    def predict(self, X, y=None, **predict_params):
        d = pairwise_distances(self.X, X, metric='cosine')
        d = d / d.sum(axis=1)[:, np.newaxis] #normalize
        return d.sum(axis=0)


