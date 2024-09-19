#!/bin/bash

# copy the 'setup' directory from the e-mission-server repo
git clone -n --depth=1 --filter=tree:0 https://github.com/e-mission/e-mission-server.git
cd e-mission-server
git sparse-checkout set --no-cone setup
git checkout
cp -r setup ../
cd ..
rm -rf e-mission-server

# determine platform 
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    TARGET_PLATFORM="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    TARGET_PLATFORM="mac"
else
    echo "Unsupported platform $OSTYPE"
    exit 1
fi

# set up conda using the e-mission-server scripts
. setup/setup_conda.sh $TARGET_PLATFORM
. setup/activate_conda.sh

# create the emcommon environment
conda env update -n emcommon -f bin/environment.yml

# install node packages
npm i
