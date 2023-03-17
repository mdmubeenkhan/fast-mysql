from jose import JWTError, jwt
from datetime import datetime, timedelta

#Secret key, we can generate secret key with command "openssl rand -hex 32"
#Algorithm
#Experation time

SECRET_KEY = "ed65cdf37d8ae47e7bd84d23fe1a9fc5a94615b6ccc06835027084685546fa6d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now()+timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


