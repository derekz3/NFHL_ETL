#!/bin/bash


# Install miniconda
CONDA=$(conda -V)
CREQ='conda 4.' # require conda >= 4.0.0
if [[ "$CONDA" != *"$CREQ"* ]]; then
  curl "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-MacOSX-x86_64.sh" -o miniconda_installer.sh
  bash miniconda_installer.sh -b -f -p $HOME/miniconda3
  rm miniconda_installer.sh
fi


# Create environment - empty conda environment + configs
CONDA_ENVS=$(conda env list)
ENV='pipe'
if [[ "$CONDA_ENVS" != *"$ENV"* ]]; then
  conda create --no-default-packages -n pipe python=3.9 -y
  conda init zsh
  conda config --env --add channels conda-forge
  conda config --set channel_priority strict
  conda install --name pipe jsonschema -y
  conda install --name pipe glob2 -y
  conda install --name pipe gsutil -y
  conda install --name pipe google-cloud-bigquery -y
  conda install --name pipe python-chromedriver-binary -y
  conda install --name pipe selenium -y
  conda install --name pipe fiona -y
  conda install --name pipe gdal -y
  conda install --name pipe geopandas -y
fi
# If you wish to explore in Jupyter Notebooks:
  # conda install -c conda-forge --name pipe descartes -y
  # conda install -c conda-forge --name pipe jupyter -y
