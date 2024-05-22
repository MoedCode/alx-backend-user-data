#!/usr/bin/python3
from flask import request
class Auth:
 def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
     return False