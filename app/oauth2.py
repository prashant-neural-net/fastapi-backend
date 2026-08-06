from jose import JWTError, jwt
from datetime import datetime, timedelta
#secret key
#algorithm
#expiration time of token
SECRET_KEY = "4ee67ca6a7e5c108ea6964c22897a0fc497b8c800c207c82588a4d3f82c29223"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt