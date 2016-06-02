import re
import string
import sklearn as sk
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
        self.X = X

    def predict(self, X, y=None, **predict_params):
        return pairwise_distances(self.X, X, metric='cosine')


