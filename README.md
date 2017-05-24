# Flask Microservices - Users Service

## Want to learn how to build this project?

Check out [testdriven.io](http://testdriven.io/).

## Want to use this project?

### Setup

1. Fork/Clone this repo

1. Download [Docker](https://docs.docker.com/docker-for-mac/install/) (if necessary)

1. Make sure you are using a Docker version >= 17:

    ```sh
    $ docker -v
    Docker version 17.03.0-ce, build 60ccb22
    ```

### Build and Run the App

Build the images:

```sh
$ docker-compose build
```

Run the containers:

```sh
$ docker-compose up -d
```

Create db:

```sh
$ docker-compose run names-service python manage.py recreate_db
```

Seed:

```sh
$ docker-compose run names-service python manage.py seed_db
```

### Commands

Run tests:

```sh
$ docker-compose run names-service python manage.py test
```

To stop the containers:

```sh
$ docker-compose stop
```

To bring down the containers:

```sh
$ docker-compose down
```

Want to force a build?

```sh
$ docker-compose build --no-cache
```

Remove images:

```sh
$ docker rmi $(docker images -q)
```
