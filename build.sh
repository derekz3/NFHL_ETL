#!/bin/bash


# Install miniconda
CONDA=$(conda -V)
CREQ='conda 4.' # require conda >= 4.0.0
if [[ "$CONDA" != *"$CREQ"* ]]; then
  curl "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-MacOSX-x86_64.sh" -o miniconda_installer.sh
  bash miniconda_installer.sh -b -f -p $HOME/miniconda3
  rm miniconda_installer.sh
  export PATH="$HOME/miniconda/bin:$PATH"
fi


# Create environment - empty conda environment + configs
CONDA_ENVS=$(conda env list)
ENV='pipe'
if [[ "$CONDA_ENVS" != *"$ENV"* ]]; then
  conda create --no-default-packages -n pipe python=3.9 -y
  conda init zsh
  conda config --env --add channels conda-forge
  conda config --set channel_priority strict
  conda install --name pipe gdal -y
fi

# conda install --name pipe jsonschema -y
# conda install --name pipe glob2 -y

# Dependencies for web crawler approach
# conda install --name pipe python-chromedriver-binary -y
# conda install --name pipe selenium -y


# Dependencies to directly query shape file with geopandas 
# conda install --name pipe fiona -y
# conda install --name pipe geopandas -y


# If you wish to explore in Jupyter Notebooks:
# conda install -c conda-forge --name pipe descartes -y
# conda install -c conda-forge --name pipe jupyter -y
