#!/usr/bin/env python3

from local_storage import LocalStorage
storage = LocalStorage()
storage.caching()
x = {"a1,b2": {'A':1, 'b':2}, "c3.d4":{'c':3, 'd':4}}
id = storage.save(x)[0]
storage.commit()
X = storage.get_by_id(id)
print(x)
y = storage.get_by_kwargs("a1,b2",all_res=True)
print(f"y = {y}")