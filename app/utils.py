from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(pwd: str):
    return pwd_context.hash(pwd)


def verify_pwd(pwd, hpwd):
    return pwd_context.verify(pwd, hpwd)
