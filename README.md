# ![PixelPerfect](frontend/src/assets/favicon-32x32.png "PixelPerfect") PixelPerfect
![GitHub Release](https://img.shields.io/github/v/release/jboelen/PixelPerfect?logo=github)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/jboelen/PixelPerfect/total?logo=github)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jboelen/PixelPerfect/build-package-publish.yml?branch=main&logo=github)
![GitHub License](https://img.shields.io/github/license/jboelen/PixelPerfect)
![Docker Image Version](https://img.shields.io/docker/v/jboelen/pixelperfect?sort=semver&logo=docker)

**PixelPerfect** is a free web-based photo-management solution, featuring:
* Responsive [Angular] webinterface
* Rest-API webservice based on [FastAPI] written in Python
* Support for various image formats including [Exif] data

Developed as an alternative to solutions such as [Lychee] to better fit my personal 
feature requirements and technology stack.

## Installation
The application can be deployed using Docker, the image is available on [Docker Hub].

```shell
docker run -d \
--name=pixelperfect \
-v /host_path/pixelperfect/data:/pixelperfect/data \
-p 8000:8000 \
jboelen/pixelperfect
```
By default, the webinterface is available on https://localhost:8000. Login with username: `admin`
password: `pixelperfect` (or username: `viewer` password: `pixelperfect`).

### Configuration Settings
Configuration settings can be set either as environment variables or using a `.env` file (mapped to the path 
`/pixelperfect/settings.env` inside the docker container).

| Setting                  | Default Value     | Description                                                                                                                                                              |
|--------------------------|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CORS_ALLOWED_ORIGINS     | `[]`              | List of [CORS] origins to allow                                                                                                                                          |
| IMAGE_RESIZE_SIZES       | `[1920]`          | List of image resolutions for which resized versions of uploaded images should be created. `1920` means a maximum resolution of `1920x1920`, preserving the aspect ratio |
| SESSION_EXPIRE_SECONDS   | `86400` (1 day)   | Maximum duration of a login sessions                                                                                                                                     |
| SQLALCHEMY_DATABASE_FILE | `pixelperfect.db` | Filename of the SQLite database                                                                                                                                          |

### Important: Reset Initial Password(s)
The initial password of the `admin` and `viewer` user can be reset from the commandline:

```shell
docker exec -ti pixelperfect pixelperfect reset-password-admin
docker exec -ti pixelperfect pixelperfect reset-password-viewer
```

## Contributions
This application was originally developed as a hobby project for personal use. 
Although feature requests, bug reports and pull requests are appreciated, I am not 
planning to expand the project much beyond its originally scope. If you see potential
and want to extend the feature set it's probably better to fork the project.

[Angular]: https://angular.io/
[CORS]: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
[Docker Hub]: https://hub.docker.com/repository/docker/jboelen/pixelperfect
[Exif]: https://en.wikipedia.org/wiki/Exif
[FastAPI]: https://fastapi.tiangolo.com/
[Lychee]: https://github.com/LycheeOrg/Lychee
