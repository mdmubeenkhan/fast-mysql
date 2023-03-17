from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(password:str):
    return pwd_context.hash(password)

# plain password will be hashed befor it can be compared with hashed pwd coming from db
def verify_pwd(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)