#!/bin/sh
PWD=$(pwd)
ID=$(docker run -d -v $PWD:/var/home mongo)
docker exec -it $ID bash
