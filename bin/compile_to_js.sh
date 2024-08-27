#!/bin/bash

. setup/activate_conda.sh && conda activate emcommon

set -e

# if '-f' (force compile), remove the old files before compiling
if [[ " $* " == *" -f "* ]]; then
    echo "-- Removing old files..."
    rm -rf ./emcommon_js/*
fi

echo "-- Compiling Python to JavaScript..."
transcrypt --nomin --ecom --xreex ./src/index.py -od ../emcommon_js

echo "-- Generating TypeScript declaration files..."
npx tsc

echo "Done"
