from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:yash@localhost:5432/fastapi_test"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# code to create the session


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    
def test_root():
    res = client.get("/")
    assert res.json().get('message') == 'jai mata di'

def test_create_users():
    res = client.post(
        "/users/", json={"email": "yabs@gmail.com", "password": "1234567890"} 
    )
    assert res.status_code == 201 or 409

def test_duplicate_user():
    res = client.post(
        "/users/", json={"email": "yabs@gmail.com", "password": "1234567890"} 
    )
    assert res.status_code == 409   
        

