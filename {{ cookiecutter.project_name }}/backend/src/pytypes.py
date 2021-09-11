import json
from enum import Enum
from typing import List, Set, Dict, Tuple, Optional, Union, NewType, Any
import attr
from pprint import pprint
import flask_login
import traceback


class ElementCannotBeUsedForMongoSchemaCreationError(Exception): pass

# @attr.s(auto_attribs=True)
@attr.s
class V():
    def toDict(self):
        '''
        ready for jsonify
        '''
        d = self.__dict__.copy()
        for k, v in d.items():
            if isinstance(v, V):
                d[k] = v.toDict()
            if isinstance(v, Enum):
                d[k] = v.name
            if isinstance(v, list):
                d[k] = [e if not isinstance(e, V) else e.toDict() for e in v]
            if isinstance(v, dict):
                d[k] = {kk: vv.toDict() if isinstance(vv, V) else vv for kk, vv in v.items()}
        return d
    
    def toBsonDict(self):
        '''
        ready for mongodb with custom informations for using V.decode
        in order to retrieve the same types when decoding from the database.
        the generated bson document should follow the mongodb schema created by the 
        static method 'createMongoSchema'
        '''
        d = self.__dict__.copy()
        try:
            d['_id'] = self.id
            del d['id']
        except Exception:
            pass
        for k, v in d.items():
            if isinstance(v, list):
                d[k] = [ (el.toBsonDict() if isinstance(el, V) else el) for el in v ]
            elif isinstance(v, V):
                d[k] = v.toBsonDict()
            elif isinstance(v, Enum):
                d[k] = {'_type': 'enum', 'data': str(v)}
        return ({
            **{'_type': str(type(self).__name__)},
            **d
        })
    
    def __repr__(self):
        return str(self.toDict())
    @staticmethod
    def decode(e):
        '''
        Transforms an arbitrarily nested structure of Vs and regular values into the Classes they should be represented by.
        '''
        if type(e)==dict:
            if '_type' in e.keys():
                if e['_type'] == "enum":
                    return eval(e['data'])
                
                e_type = e['_type']
                del e['_type']
                
                if '_id' in e.keys():
                    e['id'] = e['_id']
                    del e['_id']
            
                e = {k: V.decode(v) for k, v in e.items()}
                return eval(e_type)(**e)
            else:
                e = {k: V.decode(v) for k, v in e.items()}
                return e
        elif type(e)==list:
            return [V.decode(ee) for ee in e]
        else:
            return e
        
    @staticmethod
    def createMongoSchema(e):
        def attr_is(t):
            def f(a):
                return '__origin__' in a.__dict__.keys() and a.__origin__ == t
            # return '_name' in a.__dict__.keys() and  a._name == 'List'
            return f
        attr_is_a_list = attr_is(list)
        attr_is_a_union = attr_is(Union)
        try:
            ## basic types
            print("oOoOoOoO", e)
            if e in [str, int, float, bool, None]:
                return dict( bsonType= {str: 'string',
                                        int: 'int',
                                        float: 'double',
                                        None: "null",
                                        bool: "bool"
                                        }[e])
            ## multiple types possible
            elif attr_is_a_union(e):
                return dict(
                    bsonType="object",
                    anyOf=[ V.createMongoSchema(e) for e in e.__args__ ]
                )
            ## list of elements
            elif attr_is_a_list(e):
                return dict( bsonType="array", items=V.createMongoSchema(e.__args__[0]) )
            elif attr_is(Dict)(e):
                ##### TODO FIX THIS
                return dict(
                    bsonType="object",
                    properties=dict(
                        _type="dict",
                        values=V.createMongoSchema(List[ attr.fields(Record)[-1].type.__args__[0], attr.fields(Record)[-1].type.__args__[1] ])
                    )
                    # properties={k: createMongoSchema(v) for k, v in }
                )
            ## recurse
            elif issubclass(e, Enum):
                return dict(
                    bsonType="object",
                    properties=dict(
                        _type=V.createMongoSchema(str),
                        data=V.createMongoSchema(str)
                    )
                )
            elif issubclass(e, V):
                ans = dict(
                    bsonType="object",
                    properties={
                        ee.name : V.createMongoSchema(ee.type)
                        for ee in attr.fields(e)
                        if ee.name != "id"
                    }
                )
                
                ## convert "id" field to "_id" so that it is recognized by mongo as the id field
                if 'id' in [ee.name for ee in attr.fields(e)]:
                    ans['properties']['_id'] = V.createMongoSchema([ee for ee in attr.fields(e) if ee.name=='id'][0].type)
                    
                ## add a "_type" field for V.decode
                ans['properties']['_type'] = V.createMongoSchema(str)
                
                ## possibility to add custom data with attrs metadata field
                for ee in attr.fields(e):
                    if "mongo" in ee.metadata.keys():
                        if ee.metadata["mongo"].get("fk", False):
                            ## foreing key: the ID field refering to the object is going to be used instead of the actual instance
                            ans['properties'][ee.name] = dict(bsonType="string")
                            if attr_is_a_list(ee.type):
                                ans['properties'][ee.name] = dict( bsonType="array", items=dict(bsonType="string"))
                            
                return ans
            ## enum are represented as a list of their possible values
            elif issubclass(e, Enum):
                return dict(enum=e._member_names_)
            print('xXxXxXxXxXxXxXxX')
            print(e)
            raise ElementCannotBeUsedForMongoSchemaCreationError
        except Exception as ex:
            print('e:', e)
            raise ex


UserId = str

@attr.s(auto_attribs=True)
class User(flask_login.UserMixin):
    id: UserId
    password: str
    email: str
    admin: attr.ib(default=False)
    def __repr__(self):
        return f'{self.id} (self.email)'
