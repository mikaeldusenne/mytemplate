import yaml
import glob
import os


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
