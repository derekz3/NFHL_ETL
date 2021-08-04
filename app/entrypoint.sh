#!/bin/bash --login 
    # (The --login ensures the bash configuration is loaded, enabling Conda.)

set -eo pipefail
# set -euxo pipefail

# `exec "$@"` to let the following process take over

# Activate conda environment
conda activate pipe
