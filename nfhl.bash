#!/bin/bash

git clone https://github.com/derekz3/NFHL_ETL.git pipeline
cd pipeline
python3 -m venv test-env
source test-env/bin/activate

for line in $(cat requirements.txt)
do
  pip3 install $line -E test-env
done


# pip3 install -r requirements.txt
# python3 extract.py
# deactivate
# rm -r test-env