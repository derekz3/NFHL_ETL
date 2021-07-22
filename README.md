# NFHL ETL Pipeline  


## Summary

- **E**: This repo uses the Selenium WebDriver protocol, configured for the Google Chrome web browser, to scrape the National Flood Hazard Layer (NFHL) from the FEMA Map Service Center (MSC).
- **T**: Revelant layers will be selected from the NFHL data and converted to GeoJSON format via QGIS.
- **L**: The GeoJSON file will be uploaded to a Google Cloud Storage bucket to further explore, clean and prepare the data for analysis.

*** ***I'VE ONLY DONE 'E'—extract SO FAR***  


## Setup

1. `git clone https://github.com/derekz3/NFHL_ETL.git pipeline`
2. `cd pipeline`
3. `python3 pipe.py`
4. Enter password when/if prompted.

*...and once you're done*

5. `deactivate`
6. `rm -r pipe-test`
7. Check `~/Downloads` for the `06037C_20210601` folder.  


## Update `main` Branch

1. git add -A
2. git commit -m "[*commit message*]"
3. git push origin main