FROM python:3.11

# set environment variables
ENV BASE_DIRECTORY=/pixelperfect/data

# set work directory
WORKDIR /pixelperfect

# install pip package
COPY pixelperfect-*.tar.gz .
RUN pip install --no-cache-dir pixelperfect-*.tar.gz[all]

# copy entrypoint script
copy docker/entrypoint.sh .

HEALTHCHECK CMD curl --fail http://localhost:8000/api/health || exit 1
EXPOSE 8000/tcp
ENTRYPOINT ["/pixelperfect/entrypoint.sh"]
