#!/bin/bash


if [[ "${PORT}" == "" ]]; then
    echo "need PORT"
    exit 1
fi

docker run -it --rm --net=host \
       -e PORT="${PORT}" \
       -e PREFIX="${PREFIX}" \
       tengelisconsulting/lorenz
