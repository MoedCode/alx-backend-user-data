#!/usr/bin/env python3

from auth1 import Auth
from user import User
from db import DB
AUTH = Auth()
db = DB()
usr = AUTH.register_user("zikaMagansa@gmail.com", "Magans123")
usr1 = AUTH.register_user("mizoaTarapise@gmail.com", "tarapise123")

res = AUTH._db.find_by1(User,  False, **usr1.to_dict() )
print(f":: res >> {res.to_dict()}")
res1 = db.find_user_by(**usr.to_dict())
print(f":: res1 >> {res1.to_dict()}")
