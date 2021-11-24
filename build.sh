#!/bin/bash

docker build . -t moirai
did=$(docker create moirai:latest)
docker cp "$did:/ARM.doc" ./
docker cp "$did:/Mips.doc" ./
docker rm "$did"
