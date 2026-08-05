from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "password123"

hashed = pwd_context.hash(password)

print(hashed)
