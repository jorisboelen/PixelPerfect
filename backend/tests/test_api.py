from fastapi.testclient import TestClient
from pixelperfect.app import app
from pixelperfect.db.models import Album
from random import choice
from .fixtures import *

client = TestClient(app)


class TestAnonymous:
    def test_get_docs(self):
        response = client.get("/api/docs")
        assert response.status_code == 200

    def test_get_health(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}

    def test_post_login_incorrect_password(self, users):
        test_user = choice(users['incorrect_password'])
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Invalid username and/or password'}

    def test_post_login_incorrect_username(self, users):
        test_user = choice(users['incorrect_username'])
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Invalid username and/or password'}

    def test_get_users_me(self):
        response = client.get("/api/users/me")
        assert response.status_code == 403
        assert response.json() == {'detail': 'Not logged in'}


class TestExpired:
    def test_get_users_me(self, user_tokens):
        client.cookies = {'session_token': choice(user_tokens['incorrect']).token}
        response = client.get("/api/users/me")
        assert response.status_code == 403
        assert response.json() == {'detail': 'Session token invalid or expired'}


class TestAdmin:
    def test_post_login(self, users):
        test_user = users['correct'][0]
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']

    def test_post_albums(self, album_create):
        response = client.post("/api/albums/", json=album_create.model_dump())
        assert response.status_code == 201
        assert response.json().get('name') == album_create.name

    def test_put_album(self, album):
        album.name = fake.country()
        response = client.put(f"/api/albums/{album.id}", json={'name': album.name})
        assert response.status_code == 200
        assert Album.model_validate(response.json()) == album

    def test_delete_album(self, album):
        response = client.delete(f"/api/albums/{album.id}")
        assert response.status_code == 204
        response = client.get("/api/albums/")
        assert response.status_code == 200
        assert album not in [Album.model_validate(r) for r in response.json()]

    def test_get_users_me(self, users):
        test_user = users['correct'][0]
        response = client.get("/api/users/me")
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == True

    def test_post_logout(self):
        response = client.post("/api/logout")
        assert response.status_code == 204


class TestViewer:
    def test_post_login(self, users):
        test_user = users['correct'][1]
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']

    def test_get_albums(self, album):
        response = client.get("/api/albums/")
        assert response.status_code == 200
        assert album in [Album.model_validate(r) for r in response.json()]

    def test_get_album(self, album):
        response = client.get(f"/api/albums/{album.id}")
        assert response.status_code == 200
        assert Album.model_validate(response.json()) == album

    def test_get_users_me(self, users):
        test_user = users['correct'][1]
        response = client.get("/api/users/me")
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == False

    def test_post_logout(self):
        response = client.post("/api/logout")
        assert response.status_code == 204
