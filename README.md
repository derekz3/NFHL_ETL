# NFHL ETL Pipeline  


## Summary

- **E**: This repo uses the Selenium WebDriver protocol, configured for the Google Chrome web browser, to scrape the National Flood Hazard Layer (NFHL) from the FEMA Map Service Center (MSC).
- **T**: Revelant layers will be selected from the NFHL data and converted to GeoJSON format via QGIS.
- **L**: The GeoJSON file will be uploaded to a Google Cloud Storage bucket to further explore, clean and prepare the data for analysis.

*** ***I'VE ONLY DONE 'E'—extract SO FAR***  


## Run Pipeline

1. `chmod +x nfhl.bash`
2. ./nfhl.bash
3. Enter password when prompted.
4. Check `~/Downloads` for the `nfhl_layers` folder.  


## Update '`main`' Branch

1. git add -A
2. git commit -m "[*commit message*]"
3. git push origin main