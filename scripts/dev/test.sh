#!/usr/bin/env bash

docker-compose exec \
    --env TEST=true \
    api \
    python -m pytest "$@"
