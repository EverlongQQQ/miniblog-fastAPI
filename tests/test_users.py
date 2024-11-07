import pytest
import jwt
from app import schemas
from app.config import settings

def test_create_user(client):
    res = client.post("users/", 
                      json={"email":"test1@gmail.com", "password": "123456"})

    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "test1@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post("/login", 
            data={"username": test_user['email'], "password": test_user['password']})
    
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, 
                         settings.secret_key, 
                         algorithms=[settings.algorithm])
    id:str = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com', '123456', 403),
    ('test1@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, '123456', 422),
    ('test1@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    form_data = {k: v for k, v in {"username": email, "password": password}.items() if v is not None}
    print(form_data)
    res = client.post("/login", data=form_data)
    # res = client.post("/login", 
    #         data={"username": email, "password": password})
    
    assert res.status_code == status_code