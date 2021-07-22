#!/bin/bash

git clone https://github.com/derekz3/NFHL_ETL.git pipeline
cd pipeline
python3 -m venv pipe-test
source pipe-test/bin/activate
pip3 install -r requirements.txt
python3 pipe.py
deactivate
rm -r pipe-test