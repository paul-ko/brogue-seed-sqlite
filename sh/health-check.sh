#!/usr/bin/env bash

# Runs checks that rarely fail and take relatively long,
# and thus aren't set up as pre-commit hooks.

runit() {
    command=$1
    printf "Running $command...\n"
    if pipenv run $command >/dev/null 2>&1; then
        printf "$command success!\n"
    else
        printf "$command failure!\n"
        printf "Run pipenv run $command\n"
    fi
}

runit bandit
runit safety

