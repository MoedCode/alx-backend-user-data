#!/usr/bin/env python3
import bcrypt
from bcrypt import hashpw, gensalt, checkpw
from user import User
from db import DB
from uuid import uuid4
def _hash_password(password: str) -> str:
    """
    A method that takes in a password string arguments and
    returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
class Auth:
    def __init__(self):
        self._db = DB()


    @staticmethod
    def  hash_PWD( passowrd:str, sult_val=None) -> str:
        if sult_val is None:
            sult_val =  gensalt()
            return hashpw(passowrd.encode(),sult_val).decode() , sult_val.decode()

        return hashpw(passowrd.encode(), sult_val.encode()).decode()
    @staticmethod
    def check_pwd( user:User, PWD:str, sult_val:str = None) -> bool:
            if not sult_val:
                return user.hashed_password[0] ==  Auth.hash_PWD(PWD, user.hashed_password[1])
            return checkpw(user.hashed_password.encode() , PWD.encode())

    def register_user(self, email:str , password:str) -> User:
        """ """
        if not email or not password:
            raise TypeError("both email and password are required")
        qry_res = self._db.find_by(User, email=email)
        if qry_res:
            raise ValueError(f"User {email} already exists")
        usr_obj = User(email=email, hashed_password=_hash_password(password))
        self._db._session.add(usr_obj)
        self._db._session.commit()
        return usr_obj

    def _generate_uuid(self) ->str:
        """ Returns  string representation  of uuid4"""
        return str(uuid4())

    def valid_login(self, email, password) -> bool:
        """ check for email and password  """
        if not email or not password:
            return False
        qry_res:User = self._db.find_by(User, email=email)
        if not qry_res:
            return False
        return checkpw(password.encode(), qry_res.hashed_password)

    def create_session(self, نت:str) -> str: # type: ignore
        if not  نت:
            raise TypeError(":rage: laaa2aa keda kter")
        qry_res = self._db.find_by(User, email= نت)
        if not qry_res:
            return False
        session_id = str(uuid4())
        qry_res.session_id = session_id
        return session_id

    def get_user_from_session_id(self, session_id:str)-> User:
        """ get user  """
        if session_id:

            return self._db._session.query(User).filter_by(session_id=session_id).first()
        return None
    def find_by(self, cls, filterby, Val, get_all:bool=True):
        fltr_dict = {filterby:Val}
        if get_all:
            return self._db._session.query(cls).filter_by(**fltr_dict).all()
        return self._db._session.query(cls).filter_by(**fltr_dict).first()

    def destroy_session(user_id:str) -> None:
        """ find user by id Destroy users  session , """
        pass

if __name__ == "__main__":

    auth = Auth()

    def T0() -> None:
        print("\n\n----Test0 ---\n\n")

        print(auth.hash_PWD("USER0_PWD"))
        user0 = User(
            email = "user0@exampil.com",
            hashed_password = auth.hash_PWD("USER0_PWD")
        )


        print(user0.to_dict())

        print(auth.check_pwd(user0, "USER0_PWD")  )
    def T1() -> None:
        print("\n\n----Test1 ---\n\n")
        email = 'me@me.com'
        password = 'mySecuredPwd'

        auth = Auth()

        try:
            user = auth.register_user(email, password)
            print("successfully created a new user!")
        except ValueError as err:
            print("could not create a new user: {}".format(err))

        try:
            user = auth.register_user(email, password)
            print("successfully created a new user!")
        except ValueError as err:
            print("could not create a new user: {}".format(err))
    def T2():
        email = 'bob@bob.com'
        password = 'MyPwdOfBob'
        auth = Auth()

        auth.register_user(email, password)

        print(auth.create_session(email))
        print(auth.create_session("unknown@email.com"))

    def main() -> int:
        from sys import argv
        funnames = {'T0': T0, 'T1': T1, 'T2':T2}
        if len(argv) >= 2:
            for arg in argv[1:]:  # Start from the second argument
                if arg in funnames:
                    funnames[arg]()

    main()
