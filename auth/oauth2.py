from jose import JWTError, jwt
from datetime import datetime, timedelta
from schema import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


#auth url end point should be same what is implemented in auth.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

#Secret key, we can generate secret key with command "openssl rand -hex 32"
#Algorithm
#Experation time

SECRET_KEY = "ed65cdf37d8ae47e7bd84d23fe1a9fc5a94615b6ccc06835027084685546fa6d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now()+timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        role = payload.get("user_role")
        if id is None or role is None:
            raise credential_exception

        token_data = schema.TokenData(id=id, role=role)
    except JWTError as e:
        print(e)
        raise credential_exception
    except AssertionError as e:
        print(e)

    return token_data

def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credential_exception)


