from passlib.context import CryptContext

from sqlalchemy.inspection import inspect

def orm_to_dict(obj):
    return {
        column.key: getattr(obj, column.key)
        for column in inspect(obj).mapper.column_attrs
    }


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
