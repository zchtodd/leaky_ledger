# Leaky Ledger

Leaky Ledger is a fake bank application that is meant to be hacked for educational purposes.

You can [visit this guide](https://circumeo.io/blog/entry/hacking-the-leaky-ledger-bank/) to reveal the vulnerabilities present in version 1.0 of the Leaky Ledger app.

## Quickstart
### Run via VSCode
* [Command palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) (⇧⌘P) > Dev Containers: Reopen in Container
* F5 for debug
    * May need to select interpreter (e.g., `/opt/venv/bin/python`) first

### Both
* Copy `.env.example` to `.env` and change default values
* Open [localhost](localhost:8000) after starting via [Docker](#run-via-docker) or [locally](#run-manually)

### Run via Docker
* Install [Docker (Compose)](https://docs.docker.com/compose/install/) of course!
```bash
# build docker image and start containers
docker-compose up -d --build

# exec into container
docker exec -it leaky-ledger bash

# stop containers
docker-compose stop

# tear down containers, volumes, networks
docker-compose down
```

### Run manually*
* At minimum, still need a PostgreSQL server running
  * Easiest to spin one up with existing creds + Docker
```bash
docker run \
    --name=mypostgres -d \
    -it \
    --rm \
    --env-file=.env \
    -p 5432:5432 \
    postgres
```
* Local bits
```bash
# create virtual environment
python -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies
python -m pip install -r requirements.txt

# start web server
./startup.sh
```
* **NOTE**
  * ~~Won't serve images without reverse proxy~~
  * ~~And/or hacking Django `settings.py`~~
  * Appears to hydrate after a first run from Docker
    * Could be a local issue 🤔

## TODO
* [Issues](https://github.com/pythoninthegrass/leaky_ledger/issues)
* Add more documentation
  * asdf
  * poetry
* Test devcontainer
* CI/CD
  * Terraform ❤️

## Further Reading
* [Docker Compose with NginX, Django, Gunicorn and multiple Postgres databases_docker_weixin_0010034-云原生](https://devpress.csdn.net/cloudnative/62f2e850c6770329307f7363.html)
* [How to Use the Postgres Docker Official Image | Docker](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/)
* [Configuring HTTPS servers](http://nginx.org/en/docs/http/configuring_https_servers.html)
* [Dockerizing Django with Postgres, Gunicorn, and Nginx | TestDriven.io](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
* [Deploying a Django application in Docker with Nginx | by Charlie Bishop | Medium](https://medium.com/@cloudcleric/deploying-a-django-application-in-docker-with-nginx-beeed45bebb8)
* [Deploying a Django application in Docker with Nginx](https://medium.com/@cloudcleric/deploying-a-django-application-in-docker-with-nginx-beeed45bebb8)
* [bitnami/containers: Bitnami container images](https://github.com/bitnami/containers)
* [Generates self-signed certs for local development](https://gist.github.com/pythoninthegrass/b127241b67678dd8bf3e297bea992de2)
