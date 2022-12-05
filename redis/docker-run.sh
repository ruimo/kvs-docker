#!/bin/sh
PWD=$(pwd)
ID=$(docker run -d -v $PWD:/var/home redis)
docker exec -it $ID bash
