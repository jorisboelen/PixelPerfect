from fastapi.testclient import TestClient
from filecmp import cmp
from os.path import join
from pixelperfect.app import app
from pixelperfect.db.models import Album, Photo
from random import choice
from tempfile import NamedTemporaryFile
from time import sleep
from .fixtures import alembic_upgrade, album, album_create, photo, photo_files, users, user_tokens, fake
from .fixtures import RESOURCES_PATH

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

    def test_put_album_cover(self, album, photo):
        cover_photo = photo(album_id=album.id)
        response = client.put(f"/api/albums/{album.id}/cover", params={'cover_photo_id': cover_photo.id})
        assert response.status_code == 200
        assert response.json().get('cover_photo_id') == cover_photo.id

    def test_post_album_photos(self, album, photo_files):
        upload_files = [('files', open(str(p), 'rb')) for p in photo_files]
        response = client.post(f"/api/albums/{album.id}/upload", files=upload_files)
        assert response.status_code == 202
        assert sorted(response.json().get('received')) == sorted(p.name for p in photo_files)
        sleep(1)  # wait for photos to be processed
        response = client.get(f"/api/albums/{album.id}/photos")
        assert response.status_code == 200
        assert [r.get('name') for r in response.json()] == sorted(p.name for p in photo_files)

    def test_delete_photo(self, album, photo):
        album_photo = photo(album_id=album.id)
        response = client.delete(f"/api/photos/{album_photo.id}")
        assert response.status_code == 204
        response = client.get(f"/api/albums/{album.id}/photos")
        assert response.status_code == 200
        assert album_photo.name not in [r.get('name') for r in response.json()]

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

    def test_get_album_photos(self, album, photo):
        album_photo = photo(album_id=album.id)
        response = client.get(f"/api/albums/{album.id}/photos")
        assert response.status_code == 200
        assert album_photo in [Photo.model_validate(r) for r in response.json()]

    def test_get_photo(self, album, photo):
        album_photo = photo(album_id=album.id)
        response = client.get(f"/api/photos/{album_photo.id}")
        assert response.status_code == 200
        assert Photo.model_validate(response.json()) == album_photo

    def test_get_photo_image(self, album, photo):
        album_photo = photo(album_id=album.id)
        response = client.get(f"/api/photos/{album_photo.id}/image")
        with NamedTemporaryFile(mode='wb') as f:
            f.write(response.content)
            assert response.status_code == 200
            assert cmp(f.name, join(RESOURCES_PATH, album_photo.name))

    def test_get_users_me(self, users):
        test_user = users['correct'][1]
        response = client.get("/api/users/me")
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == False

    def test_post_logout(self):
        response = client.post("/api/logout")
        assert response.status_code == 204
