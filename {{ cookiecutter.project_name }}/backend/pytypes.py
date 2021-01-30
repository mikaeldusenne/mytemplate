import yaml
import copy


class Tree(yaml.YAMLObject):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'<{self.name}>'
    def walk(self, l):
        if isinstance(l, str):
            l = os.path.split(l)
        if len(l) == 0:
            return self
        else:
            x, *xs = l
            try:
                return [e for e in self.children if e.name==x][0].walk(xs)
            except Exception as e:
                print(e)
    def isLeaf(self):
        return False
    def map(self, f):
        c = copy.copy(self)
        if c.isLeaf():
            c.content = f(c.content)
        else:
            c.children = [e.map(f) for e in c.children]
        return c
    def filter(self, predicate):
        c = copy.copy(self)
        if c.isLeaf():
            if predicate(c):
                return c
        else:
            c.children = list(filter(lambda e: not e is None, [e.filter(predicate) for e in c.children]))
            return c
    def find_one(self, predicate):
        if self.isLeaf():
            if predicate(self):
                return self
        else:
            for cc in self.children:
                e = cc.find_one(predicate)
                if e is not None:
                    return e
    def find_all(self, predicate=lambda e: True):
        if self.isLeaf():
            return [self] if predicate(self) else []
        else:
            l = []
            for cc in self.children:
                l = l + cc.find_all(predicate)
            return l
    def deep_dict(self):
        ans = self.__dict__
        if not self.isLeaf():
            ans['children'] = [e.deep_dict() for e in self.children]
        return ans
    def flatten(self):
        if self.isLeaf():
            return [self]
        else:
            return [ee for e in [el.flatten() for el in self.children] for ee in e]

    
# class TreeEncoder(JSONEncoder):
#     def default(self, o):
#         # return o.deep_dict()
#         return o.__dict__

    
class Node(Tree):
    def __init__(self, name, children=[]):
        super().__init__(name)
        self.children = children
    
        
class Leaf(Tree):
    def __init__(self, name, content):
        super().__init__(name)
        self.content = content
    def __repr__(self):
        return f'> [{self.name}]'
    def isLeaf(self):
        return True

