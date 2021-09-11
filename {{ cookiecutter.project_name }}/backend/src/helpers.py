from itertools import islice, chain
import traceback
from math import floor, ceil
import yaml
import glob
import os
import logging
import pickle

def clean_str(s):
    return (s.lower().strip()
            .replace('é','e')
            .replace('è','e')
            .replace('ê','e')
            .replace('ë','e')
            .replace('î','i')
            .replace('ï','i')
            .replace('ô','o')
            .replace('ç','c')
            .replace('ù','u')
            .replace('â','a')
            .replace('à','a')
            )


def load_yaml(p):
    with open(p, 'r') as f:
        return yaml.load(f, yaml.BaseLoader)


def splitter(stuff, l):
    if len(l)==0:
        return [stuff]
    else:
        x, *xs = l
        return [ee for e in stuff.split(x) for ee in splitter(e, xs)]


def dict_get_path(d, path):
    if len(path) == 0:
        return d
    else:
        p, *ps = path
        return dict_get_path(d[p], ps)


def dict_set_path(d, path, val):
    p, *ps = path
    if len(ps) == 0:
        d[p] = val
    else:
        dt = d.get(p, {})
        if not type(dt) == dict:
            dt = {}
        d[p] = dict_set_path(dt, ps, val)
    return d
    

def subset_tree(tree, subsetter):
    d = {}
    for p in subsetter:
        dict_set_path(d, p, dict_get_path(tree, p))
    return d


def last_modified_file(p):
    fs = glob.glob(f"{p}/*")
    return sorted(fs,key=os.path.getmtime)[-1]

def load_pickle(path):
    logging.debug('loading pickle from {}'.format(path))
    with open(path, 'rb') as f:
        o = pickle.load(f)
    return o


def save_pickle(path, o):
    logging.debug('saving pickle to {}'.format(path))
    with open(path, 'wb') as f:
        pickle.dump(o, f)


def chunk(l, n=50):
    for i in range(0, len(l), n):
        yield l[i:(i + n)]

def show_progress(k, n=None, length=50, prog='=>', todo=' '):
    '''prints pretty progress'''
    details = f"{k:04}"
    if n is not None:
        ratio = k/n
        graphics = '['+max(0, floor(ratio*length)-1)*prog[:1]+prog[-1:]+(ceil((1-ratio)*length)-1) * todo+']'
        details = f"{graphics} {details}/ {n:04} ({int(ratio*100)}%)"
    print(details, end="\r")


def process_by_chunk(f, l, len_l=None, chunk_size=50, display_progress=False):
    '''
    lazy version of chunk processing. len_n has to be provided if known to show progress as a %.
    '''
    it = iter(l)
    k=0
    if display_progress and len_l is not None:
        show_progress(k, len_l)

    for first in it:
        processl = list(chain([first], islice(it, chunk_size - 1)))
        ll = f(processl)
        if ll is None:
            raise Exception(f"Chunked processing failed for chunk #{i} of {l}:\n {ch}\n-->{traceback.format_exc()}\n(f(ch) returned None)")
        k+=len(processl)
        if display_progress and len_l is not None:
            show_progress(k, len_l)
        for e in ll:
            yield e


def retry_with_delay(f, retry=5, retry_delay=1, delay_increment_factor=1.5, message_prefix="retry_with_delay"):
    try:
        return f()
    except Exception as ex:
        if retry > 0:
            logging.warning(f"{traceback.format_exc()}\n{message_prefix} failed, resuming in {retry_delay}s... (remaining attempts: {retry})")
            sleep(retry_delay)
            return retry_with_delay(f, retry-1, retry_delay*delay_increment_factor, delay_increment_factor, message_prefix)
        else:
            logging.error(f"{traceback.format_exc()}\n{message_prefix} failed after all retry attempts")
            raise ex from None

