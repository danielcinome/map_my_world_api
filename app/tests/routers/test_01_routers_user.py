

def test_create_user(client):
    response = client.post('/user/create', json={
        'username': 'test_user',
        'email': 'nametest@test.com',
        'password': 'test_password',
        'verify_password': 'test_password'
    })
    assert response.status_code == 200
    assert response.json() == {
        'username': 'test_user',
        'email': 'nametest@test.com',
        'is_active': True
    }

def test_create_user_by_username_exist(client):
    response = client.post('/user/create', json={
        'username': 'test_user',
        'email': 'nametest2@test.com',
        'password': 'test_password',
        'verify_password': 'test_password'
    })

    assert response.status_code == 400
    assert response.json().get('detail') == 'Error creating user: This username or email already exists in the system.'


def test_create_user_by_email_exist(client):
    response = client.post('/user/create', json={
        'username': 'test_user2',
        'email': 'nametest@test.com',
        'password': 'test_password',
        'verify_password': 'test_password'
    })

    assert response.status_code == 400
    assert response.json().get('detail') == 'Error creating user: This username or email already exists in the system.'

def test_get_user(client_with_auth):
    response = client_with_auth.get('/user/test_user')
    assert response.status_code == 200
    assert response.json() == {
        'username': 'test_user',
        'email': 'nametest@test.com',
        'is_active': True
    }

def test_get_user_not_found(client_with_auth):
    response = client_with_auth.get('/user/test_user_not_found')
    assert response.status_code == 404
    assert response.json().get('detail') == 'The user with this username not exists in the system.'