#!/bin/bash

. setup/activate_conda.sh && conda activate emcommon

echo "Running JavaScript tests..."

ROOT_DIR_ABSOLUTE=$(realpath)

# remove any existing test_js_* directories (from previous runs)
rm -rf $ROOT_DIR_ABSOLUTE/test_js_*


for file in test/**/test_*.py; do
    # if there is a .js file in the same directory, skip
    if [ -f "${file%.*}.js" ]; then
        echo "Found dedicated .js version of test $file, not compiling"
        continue
    else
        echo "Compiling $file"
    fi
    # filename without directory and extension
    suffix=$(basename $file)
    PYTHONPATH=./src transcrypt --nomin --ecom --xreex $file --xpath test -od $ROOT_DIR_ABSOLUTE/test_js_$suffix
done
npx node --experimental-vm-modules node_modules/jest/bin/jest.js
