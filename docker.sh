#!/usr/bin/env bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd $ROOT
trap popd EXIT

function docker_help() {
    echo "docker.sh (help|clean|build|run|all)"
}

function docker_clean() {
    rm -rf temp out
}

function docker_build() {
    docker build -t grlee/you_can_docker_a_gif .
}

function docker_run() {
    docker run -v $PWD:/usr/src/app grlee/you_can_docker_a_gif
}

function docker_all() {
    docker_clean
    docker_build
    docker_run
}


function main() {
    pushd $ROOT
    args="$1"
    for key in "$args"
    do
        case $key in
            clean)
            docker_clean
            ;;
            build)
            docker_run
            docker_build
            ;;
            run)
            docker_run
            ;;
            all)
            docker_all
            ;;
            help)
            docker_help
            ;;
            *)    # unknown option
            docker_help
            ;;
        esac
    done
}

main $@