Title: orm based on pymongo
Date: 2015-12-03 10:20
Category: python
Tags: python
Slug:orm-based-on-pymongo
Authors: Tommy.Yu
Summary: pelican plugin
# orm based on pymongo

```python
# -*- coding:utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
client = MongoClient()
db = client.test
class Model(object):
    _model=''
    _fields = []
    _base_fields=['created_date', 'updated_date']
    _required_fields = []

    def __init__(self, **value):
        self.id=None
        all_fields = list(set(self.__class__._fields + self.__class__._base_fields))
        for attr in all_fields:
            if value.get(attr, None) is None:#auto fullfill value(s)
                default_val=None
                if attr=='created_date':
                    default_val = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if attr=='updated_date':
                    continue
                value.update({attr:default_val})
            if not hasattr(self, attr):#add attributes to current object
                setattr(self, attr, value.get(attr))
        self.value=value

    def save(self):
        assert self.__class__._model, '_model attribute of %s is null or empty'%(cls.__name__)
        assert self.__class__._model in db.collection_names(), 'collection %s does not exist!'%self.__class__._model
        self.check_required_fields()
        model =getattr(db, self.__class__._model, None)

        self.__to_json()#update data from attrbitutes to self.value
        if not self.id:#new
            oid =  model.insert(self.value) if model else None
            self.id = oid#str(oid) if oid else None
        else:#update
            self.value.update({'updated_date':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            model.update_one(
                {"_id": self.id},
                {
                    "$set": self.value,
                    # "$currentDate": {"updated_date": True}
                }
            )
        return self.id#str(oid) if oid else None

    @classmethod
    def get(cls, **where):
        assert cls._model, '_model attribute of %s is null or empty'%(cls.__name__)
        assert cls._model in db.collection_names(), 'collection %s does not exist!'%cls._model
        model =getattr(db, cls._model, None)
        return model.find_one(where) if model else None

    @classmethod
    def select(cls, **where):
        assert cls._model, '_model attribute of %s is null or empty'%(cls.__name__)
        assert cls._model in db.collection_names(), 'collection %s does not exist!'%cls._model
        model =getattr(db, cls._model, None)
        return model.find(where) if model else []

    @classmethod
    def update(cls, new_value={}, **where):
        assert cls._model, '_model attribute of %s is null or empty'%(cls.__name__)
        assert cls._model in db.collection_names(), 'collection %s does not exist!'%cls._model
        model =getattr(db, cls._model, None)
        return model.update_many(where,{"$set": new_value,})

    def check_required_fields(self):
        for col in self.__class__._required_fields:
            assert getattr(self, col, None) is not None, 'field "%s" of model %s is required!'%(col, self.__class__._model)

    def __to_json(self):
        [self.value.update({attr:getattr(self, attr)}) for attr in dir(self) if attr in self._fields]

class User(Model):
    _model='user'
    _fields=['name', 'age', 'sex']
    _required_fields=['sex']

if __name__=='__main__':
    #u = User.get(_id=ObjectId("56d7bb80e5e7bd21663942e4"))

    #save test
    u = User(name='tommy', age=29)
    oid = u.save()

    #update test( update one)
    u.age=30

    #get test
    print User.get(_id=oid)

    #select test
    for u in User.select():
        print u

    #update test (update many)
    print User.update({'sex':'M'}, name='tommy')
```