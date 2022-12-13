# Asklora Banking APP v1

- [Asklora Banking APP v1](#asklora-banking-app-v1)
  - [Prerequisite](#prerequisite)
    - [Docker](#docker)
  - [How to develop](#how-to-develop)
    - [Run services](#run-services)
    - [Run pytest](#run-pytest)
    - [Reset database](#reset-database)
    - [Stop services](#stop-services)
  - [Services](#services)

## Prerequisite

### Docker

install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)

## How to develop

### Run services

> [Install docker & docker-compose](#docker) first

```sh
$ cd /path/to/project/root/dir
$ ./scripts/dev/up.sh
```


### Run pytest

> [Install docker & docker-compose](#docker) first

create user, password and database for testing
```sql
CREATE USER asklora_test WITH PASSWORD 'asklora_test';
CREATE DATABASE asklora_test;
GRANT ALL PRIVILEGES ON DATABASE asklora_test TO asklora_test;
```

```sh
$ cd /path/to/project/root/dir
$ ./scripts/dev/test.sh
```

### Reset database

> [Install docker & docker-compose](#docker) first

```sh
$ cd /path/to/project/root/dir
$ ./scripts/dev/reset-db.sh
```

### Stop services

> [Install docker & docker-compose](#docker) first

```sh
$ cd /path/to/project/root/dir
$ ./scripts/dev/down.sh
```

## Services

- [api](http://localhost:31000)
- [api auth docs](http://localhost:31000/v1/auth/docs#/default/post_login_login_post)
- [api users docs](http://localhost:31000/v1/user/docs#/)
- [db admin](http://localhost:8081/?pgsql=db&username=postgres) (password : asklora_app)
