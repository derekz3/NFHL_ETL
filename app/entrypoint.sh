#!/bin/bash --login 
    # (The --login ensures the bash configuration is loaded, enabling Conda.)

set -eo pipefail
# set -euxo pipefail

# Activate conda environment and run main.py
conda activate pipe
python3 main.py
# exec "$@" to let the following process take over
