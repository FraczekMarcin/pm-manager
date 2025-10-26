from datetime import datetime, timedelta
import os, jwt
from passlib.context import CryptContext

PWD_CTX = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET = os.getenv('SECRET_KEY', 'change_this_secret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7

def verify_password(plain, hashed):
    return PWD_CTX.verify(plain, hashed)

def get_password_hash(password):
    return PWD_CTX.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    encoded = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
