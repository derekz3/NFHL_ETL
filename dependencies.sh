#!/bin/bash

# Install miniconda if needed
https://stackoverflow.com/questions/44982520/installing-miniconda2-non-interactively
CONDA=$(conda -V)
echo $CONDA
REQ='conda 4.'
if [[ "$CONDA" != *"$REQ"* ]]; then
  curl "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-MacOSX-x86_64.sh" -o miniconda_installer.sh
  bash miniconda_installer.sh -b -f -p $HOME/miniconda3
  rm miniconda_installer.sh
fi

conda create --no-default-packages -n pipe python=3.9 -y
conda init zsh
conda activate pipe

conda config --env --add channels conda-forge
conda install -c conda-forge --name pipe selenium -y
conda install -c conda-forge --name pipe fiona -y
conda install -c conda-forge --name pipe geopandas -y

# conda install -c conda-forge descartes -y
# conda install jupyter -y

source ~/miniconda3/etc/profile.d/conda.sh
conda activate pipe
python3 transform.py

# conda deactivate
# conda env remove --name pipe