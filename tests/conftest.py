from fastapi.testclient import TestClient
import pytest
from app import models
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token

#add _test in the end of name
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# setting up test db
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    except Exception as e:
        db.close()
        raise e
    finally:
        db.close()
# setting up test client
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        except Exception as e:
            session.close()
            raise e
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {"email":"test1@gmail.com", "password": "123456"}
    res = client.post("users/", json=user_data)
    
    assert res.status_code == 201

    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"test2@gmail.com", "password": "123456"}
    res = client.post("users/", json=user_data)
    
    assert res.status_code == 201

    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "1st title",
        "content": "first content",
        "owner_id": test_user['id']
    },{
        "title": "2nd title",
        "content": "second content",
        "owner_id": test_user['id']
    },{
        "title": "3rd title",
        "content": "third content",
        "owner_id": test_user['id']
    }, {
        "title": "4rd title",
        "content": "third content",
        "owner_id": test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts

    