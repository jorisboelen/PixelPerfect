# ![PixelPerfect](frontend/src/assets/favicon-32x32.png "PixelPerfect") PixelPerfect
[![GitHub Release](https://img.shields.io/github/v/release/jorisboelen/PixelPerfect?logo=github)](https://github.com/jorisboelen/PixelPerfect/releases/latest)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/jorisboelen/PixelPerfect/total?logo=github)](https://github.com/jorisboelen/PixelPerfect/releases)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jorisboelen/PixelPerfect/build-package-publish.yml?logo=github)](https://github.com/jorisboelen/PixelPerfect/actions)
[![GitHub License](https://img.shields.io/github/license/jorisboelen/PixelPerfect)](https://github.com/jorisboelen/PixelPerfect/blob/main/LICENSE)
[![Docker Image Version](https://img.shields.io/docker/v/jboelen/pixelperfect?sort=semver&logo=docker)](https://hub.docker.com/r/jboelen/pixelperfect)

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
By default, the webinterface is available on http://localhost:8000. Login with username: `admin`
password: `pixelperfect` (or username: `viewer` password: `pixelperfect`).

### Configuration Settings
Configuration settings can be set either as environment variables or using a `.env` file (mapped to the path 
`/pixelperfect/settings.env` inside the docker container).

| Setting                  | Default Value     | Description                                                                                                                                                              |
|--------------------------|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CORS_ALLOWED_ORIGINS     | `[]`              | List of [CORS] origins to allow                                                                                                                                          |
| IMAGE_RESIZE_SIZES       | `[1920]`          | List of image resolutions for which resized versions of uploaded images should be created. `1920` means a maximum resolution of `1920x1920`, preserving the aspect ratio |
| INITIAL_PASSWORD_ADMIN   | `pixelperfect`    | Initial password for the `admin` user.                                                                                                                                   |
| INITIAL_PASSWORD_VIEWER  | `pixelperfect`    | Initial password for the `viewer` user.                                                                                                                                  |
| SESSION_EXPIRE_SECONDS   | `86400` (1 day)   | Maximum duration of a login sessions                                                                                                                                     |

#### Database Settings
By default, [SQLite] is configured as database with the following settings:

| Setting         | Default Value     | Description                                     |
|-----------------|-------------------|-------------------------------------------------|
| DATABASE_SCHEME | `sqlite`          | Can be either `mysql`, `postgresql` or `sqlite` |
| DATABASE_FILE   | `pixelperfect.db` | The filename of the SQLite database file        | 

Alternatively, [MySQL] or [PostgreSQL] can be configured as well:

| Setting             | Default Value  | Description                                                                                                                                  |
|---------------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| DATABASE_SCHEME     | `sqlite`       | Can be either `mysql`, `postgresql` or `sqlite`                                                                                              |
| DATABASE_HOST       | `localhost`    | The hostname of the database server                                                                                                          |
| DATABASE_PORT       | `n/a`          | The port of the database server, for example: `3306` or `5432`                                                                               |
| DATABASE_DB         | `pixelperfect` | The name of the database                                                                                                                     |
| DATABASE_USER       | `pixelperfect` | The username for connecting to the database server                                                                                           |
| DATABASE_PASSWORD   | `n/a`          | The password for connecting to the database server                                                                                           |
| DATABASE_PARAMETERS | `n/a`          | Additional parameters to add to the database connection url. For example to enable TLS/SSL: `ssl_ca=ca-certificate.pem` or `sslmode=require` |

#### Storage Settings
By default, files are stored on the local filesystem. This includes the database (in case of SQLite) and media files:

| Setting         | Default Value               | Description                                     |
|-----------------|-----------------------------|-------------------------------------------------|
| BASE_DIRECTORY  | `/pixelperfect/data`        | The base directory for storing persistent files |
| IMAGE_DIRECTORY | `/pixelperfect/data/images` | The directory for storing image files           | 

Alternatively, image files can also be stored in [S3]:

| Setting         | Example Value                            | 
|-----------------|------------------------------------------|
| IMAGE_DIRECTORY | `s3://s3-bucket-name/optional-subfolder` | 


### Reset Initial Password(s)
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
[Docker Hub]: https://hub.docker.com/r/jboelen/pixelperfect
[Exif]: https://en.wikipedia.org/wiki/Exif
[FastAPI]: https://fastapi.tiangolo.com/
[Lychee]: https://github.com/LycheeOrg/Lychee
[MySQL]: https://www.mysql.com/
[PostgreSQL]: https://www.postgresql.org/
[S3]: https://aws.amazon.com/s3/
[SQLite]: https://www.sqlite.org/
