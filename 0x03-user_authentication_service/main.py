from bcrypt import hashpw, gensalt, checkpw
from user import User

class AuthService:
    @staticmethod
    def _hash_password(password: str, salt: str = None) -> tuple:
        """Hash a password with a provided or new random salt."""
        if salt is None:
            salt = gensalt().decode()  # Generate a new salt if none is provided
        hashed_password = hashpw(password.encode(), salt.encode()).decode()
        return hashed_password, salt

    @staticmethod
    def check_pwd(user: User, plain_password: str) -> bool:
        """Check if the provided plain password matches the stored hashed password."""
        if user and user.hashed_password:
            return checkpw(plain_password.encode(), user.hashed_password.encode())
        return False

if __name__ == "__main__":
    auth_service = AuthService()

    # Hashing and verifying password
    hashed_password, salt = auth_service._hash_password("USER0_PWD")
    print(f"Hashed password: {hashed_password}, Salt: {salt}")

    user0 = User()
    user0.email = "user0@exampil.com"
    user0.hashed_password = hashed_password

    print(user0.to_dict())

    # Checking password
    print(auth_service.check_pwd(user0, "USER0_PWD"))  # Should return True
    print(auth_service.check_pwd(user0, "WRONG_PWD"))  # Should return False
