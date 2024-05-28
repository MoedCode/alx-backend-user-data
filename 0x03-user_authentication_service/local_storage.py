#!/usr/bin/env python3
import uuid
import json
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"


class LocalStorage:
    __session = {}
    __file_path = "local_storage.json"
    def __init__(self, file_path=None):
        self.file_path = file_path or self.__file_path

    def save(self, object):
        if isinstance(object, dict):
            object["id"] = object.get("id") or str(uuid.uuid4())
            object["created_at"] = object.get("created_at") or datetime.now().strftime(time)
            key = "Dict__" + str(object["id"]) + "__" + str(object["created_at"])
            self.__session[key] = object
            return object["id"], object["created_at"]
        else:
            if not hasattr(object, "id"):
                object.id = str(uuid.uuid4())
            key = object.id + "." + object.__class__.__name__
            self.__session[key] = object
        # print(f"session fom save f{self.__session}")



    def caching(self):
        cached = {}
        with open(self.file_path, 'r') as F:
            cached= json.load(F)
        if cached:
            for key in cached:
                self.__session[key] = cached[key]
        # print(f"cached data {cached}")
        # print(f"cached data from session  {self.__session}")


    def commit(self):
        json_objects = {}
        for key in self.__session:
            if not key.startswith("Dict__"):
                if hasattr(self.__session[key], "to_dict") and callable(getattr(self.__session[key], "to_dict")):
                    json_objects[key] = self.__session[key].to_dict()
                else:
                    json_objects[key] = self.__session[key].__dict__

            else:
                json_objects[key] = self.__session[key]

        with open(self.file_path, 'w') as f:  # Use self.__file_pat
            json.dump(json_objects,f,indent=1 )
    def get_by_id(self,  id):
        if id:
            self.caching()
            for key in self.__session:
                if id in key:
                    return self.__session[key]
            return None

    def get_by_kwargs(self, *args, all_res=True, **kwargs):
        print(args)
        matching = {}
        if not args and not kwargs:
            raise ValueError("no value passed")
        self.caching()
        if args or kwargs:
            if kwargs and not args:
                args = kwargs.values()
            if all_res:
                for key in self.__session:
                    for arg in args:
                        if arg in self.__session[key].values():
                            matching[key] = self.__session[key]
            else:
                matching = {key: self.__session[key] for key in self.__session
                            if all(value in self.__session[key].values() for value in args)}
        return matching

    @staticmethod
    def compare_dict_values(dict1, dict2):
        if dict1.keys() != dict2.keys():
            return False
        for key in dict1:
            if dict1[key] != dict2[key]:
                return False
        return True

    def all_values_exist_in_dict(self, dictionary, *args):
        dict_values = set(dictionary.values())
        return all(value in dict_values for value in args)

# Test script (local_storage_tst.py)
if __name__ == "__main__":
    storage = LocalStorage()
    storage.caching()
    x = {"username":"kwada", "age":"27"}
    id = storage.save(x)[0]
    storage.commit()
    result1 = storage.get_by_id(id)
    print(result1)
    result2 = storage.get_by_kwargs("kayouko", all_res=True)
    print(f"result2 = {result2}")

    # Test all_values_exist_in_dict method
    dictionary = {"Key0": "value0", "Key1": "value1", "Key2": "value2", "Key3": "value3"}
    print(storage.all_values_exist_in_dict(dictionary, "value1", "value3"))  # Output: True

        # print(f"session fom commit f{self.__session}")
        # print(f"session fom commit to commit {json_objects}")

'''
def to_jason(self, object={}, cls=None):
    cls_name = ""
    obj_id = ""
    if not object:
        raise ValueError("object cannot be none")
    if not cls:
        cls = object.__class__.__name__
    if cls and type(cls) is not str:
        cls_name = str(cls.__name__)
    if object.id:
        obj_id = object.id
    else:
        obj_id = str(uuid.uuid4)
        object.id = obj_id
    key = obj_id + "." + cls_name
    self.__session[key] = object
'''
'''
        if not object or not object.__class__.__name__:
            raise TypeError(f"object cant be None, must have  __class__.__name__")
        if not id and not object.id:
            raise KeyError("object must have id must passed ,")
        key = object.id + "." + object.__class__.__name__
'''