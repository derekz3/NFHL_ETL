#!/bin/bash


# Install Google Chrome - https://superuser.com/questions/602680/how-to-install-google-chrome-from-the-command-line
CHROME=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version)
GREQ='Google Chrome 92.' # require Google Chrome >= 92.0.4515
if [[ "$CHROME" != *"$GREQ"* ]]; then
  wget https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg
  open ~/Downloads/googlechrome.dmg
  sudo cp -r /Volumes/Google\ Chrome/Google\ Chrome.app /Applications/
  rm googlechrome.dmg
fi


# Install miniconda - https://stackoverflow.com/questions/44982520/installing-miniconda2-non-interactively
CONDA=$(conda -V)
CREQ='conda 4.' # require conda >= 4.0.0
if [[ "$CONDA" != *"$CREQ"* ]]; then
  curl "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-MacOSX-x86_64.sh" -o miniconda_installer.sh
  bash miniconda_installer.sh -b -f -p $HOME/miniconda3
  rm miniconda_installer.sh
fi


# Create script environment if needed - empty conda environment + configs
# Install required packages - https://gist.github.com/shravan-kuchkula/778e90eef818aa955676963c0132f08b
# Install chromedriver - https://stackoverflow.com/questions/38876281/anaconda-selenium-and-chrome/55973176
CONDA_ENVS=$(conda env list)
ENV='pipe'
if [[ "$CONDA_ENVS" != *"$ENV"* ]]; then
  conda create --no-default-packages -n pipe python=3.9 -y
  conda init zsh
  conda config --env --add channels conda-forge
  conda install -c conda-forge --name pipe python-chromedriver-binary -y
  conda install -c conda-forge --name pipe selenium -y
  conda install -c conda-forge --name pipe fiona -y
  conda install -c conda-forge --name pipe geopandas -y
fi


# If you wish to explore in Jupyter Notebooks:
# conda install -c conda-forge descartes -y
# conda install jupyter -y


# Run transform script in conda environment
# https://stackoverflow.com/questions/55507519/python-activate-conda-env-through-shell-script
source ~/miniconda3/etc/profile.d/conda.sh
conda activate pipe
python3 extract.py
python3 transform.py


# conda deactivate
# conda env remove --name pipe