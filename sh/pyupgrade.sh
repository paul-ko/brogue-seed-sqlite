#!/usr/bin/env bash

# Runs pyupgrade.
# I get permissions errors when I run it against a directory, so find and xargs are used
# to avoid this problem.

find ./broguedb -path "*.py" | xargs pyupgrade

