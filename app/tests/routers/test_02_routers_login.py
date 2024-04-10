

def test_login(client):
    response = client.post('/login/access-token', data={
        'username': 'test_user',
        'password': 'test_password'
    })
    assert response.status_code == 200
    assert response.json().get('access_token')
    assert response.json().get('token_type') == 'bearer'

def test_login_wrong_password(client):
    response = client.post('/login/access-token', data={
        'username': 'test_user',
        'password': 'test_password_wrong'
    })
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'

def test_login_wrong_username(client):
    response = client.post('/login/access-token', data={
        'username': 'test_user_wrong',
        'password': 'test_password'
    })
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'    