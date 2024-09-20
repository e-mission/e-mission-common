#!/bin/bash

# Check if conda exists
if ! command -v conda &> /dev/null; then
    echo "conda could not be found"
    return 1
fi

# Determine platform and architecture
ARCH=$(uname -m)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [[ "$ARCH" == "x86_64" ]]; then
        TARGET_PLATFORM="Linux-x86_64"
    elif [[ "$ARCH" == "aarch64" ]]; then
        TARGET_PLATFORM="Linux-aarch64"
    else
        echo "Unsupported architecture $ARCH on Linux"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ "$ARCH" == "x86_64" ]]; then
        TARGET_PLATFORM="MacOSX-x86_64"
    elif [[ "$ARCH" == "arm64" ]]; then
        TARGET_PLATFORM="MacOSX-arm64"
    else
        echo "Unsupported architecture $ARCH on macOS"
        exit 1
    fi
else
    echo "Unsupported platform $OSTYPE"
    exit 1
fi

# copy the 'setup' directory from the e-mission-server repo
git clone -n --depth=1 --filter=tree:0 https://github.com/e-mission/e-mission-server.git
cd e-mission-server
git sparse-checkout set --no-cone setup
git checkout
cp -r setup ../
cd ..
rm -rf e-mission-server

# set up conda using the e-mission-server scripts
. setup/setup_conda.sh $TARGET_PLATFORM
. setup/activate_conda.sh

# create the emcommon environment
conda env update -n emcommon -f bin/environment.yml

# install node packages
npm i
