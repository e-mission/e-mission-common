#!/bin/bash

. setup/activate_conda.sh && conda activate emcommon

PYTHONPATH=./src pytest test --asyncio-mode=auto
