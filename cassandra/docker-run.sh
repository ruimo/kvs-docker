#!/bin/sh
PWD=$(pwd)
ID=$(docker run -d -v $PWD:/var/home cassandra)
docker exec -it $ID bash
