import os
import sys
import wget
import glob
import time
import geopandas
import subprocess
from zipfile import ZipFile


# Install miniconda on M1 MAC
CONDA = os.popen('conda -V').read().split('\n')[0].strip()
if 'conda 4.' not in CONDA:
    os.system('curl "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-MacOSX-x86_64.sh" -o miniconda_installer.sh')
    os.system('bash miniconda_installer.sh -b -f -p $InstallDirectory')
    os.system('rm miniconda_installer.sh')


# Install geopandas using pip
# pip3 install Fiona
# pip3 install Shapely
# pip3 install pyproj
# pip3 install Rtree
# pip3 install geopandas






# os.chdir("../nfhl_layers")
# os.system("find . -depth 1 -type f -not -name '*.shp' -delete")
# os.system("find . -depth 1")