#!/usr/bin/env bash

docker build -t grlee/you_can_docker_a_gif . && docker run -v $PWD:/usr/src/app grlee/you_can_docker_a_gif
