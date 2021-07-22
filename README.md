# NFHL ETL Pipeline
- E: The repo uses the Selenium WebDriver protocol, configured for the Google Chrome web browser, to scrape the National Flood Hazard Layer (NFHL) from the FEMA Map Service Center (MSC).
- T: Revelant layers will be selected from the NFHL data and converted to GeoJSON format via QGIS.
- L: The GeoJSON file will be uploaded to a Google Cloud Storage bucket to further explore, clean and prepare the data for analysis.

***I'VE ONLY DONE 'E'--extract SO FAR***

## Setup
1. `git clone repo`
2. `cd repo`
3. `pip3 install -r requirements.txt`
4. `python3 -m venv pipe-test`
5. `source pipe-test/bin/activate`
6. `python3 pipe.py`
7. Enter password when prompted.

*...and once you're done*
8. `rm -r venv`
9. Check `~/Downloads` for `06037C_20210601.zip`