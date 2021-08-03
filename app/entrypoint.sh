#!/bin/bash --login 
    # (The --login ensures the bash configuration is loaded, enabling Conda.)
# set -euo pipefail
set -e

# Activate conda environment and let the following process take over
conda activate pipe
exec "$@"
