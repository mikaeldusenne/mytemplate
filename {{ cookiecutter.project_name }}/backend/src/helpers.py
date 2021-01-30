import numpy as np
import pandas as pd
from functools import reduce
import pickle

def load_pickle(path):
    logging.debug('loading pickle from {}'.format(path))
    with open(path, 'rb') as f:
        o = pickle.load(f)
    return o

def save_pickle(path, o):
    logging.debug('saving pickle to {}'.format(path))
    with open(path, 'wb') as f:
        pickle.dump(o, f)


def isnpnan(e):
    return type(e)==float and np.isnan(e)


def issomekindofnone(e, alsostr=None):
    if alsostr is not None and type(alsostr) != list:
        alsostr = [alsostr]
    return isnpnan(e) or pd.isna(e) or e is None or (alsostr is not None and e in alsostr)


def replaceNaNone(e, naval):
    return naval if issomekindofnone(e) else e


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colored(e, color):
    return(f"{color}{e}{bcolors.ENDC}")


def curry(f):
    def g(e):
        return f(*e)
    return g


class Either():
    def __init__(self, left=None, right=None):
        self.left=left
        self.right=right
    def mappend(self, e, f):
        self.left=f(self.left, e.left)
        self.right=f(self.right, e.right)
        return self
    def __repr__(self):
        return f"Left[{self.left}]Right[{self.right}]"


def listAppendNoNone(l, e):
    return l if e is None else l+[e]


def combineEithers(f):
    def g(a,b):
        # print("combine eithers", a, b)
        return a.mappend(b, f)
    return g


def combineEithersToList(l) -> Either:
    return reduce(combineEithers(listAppendNoNone), l, Either(right=[], left=[]))




