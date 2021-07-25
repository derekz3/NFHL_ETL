# NFHL ETL Pipeline  


**I'VE DONE: 'E'—extract and 'T'-transform so far**
**NEXT STEP: 'Dockerize' these services + Deploy with Cloud Run**


## Summary

- **E**: This repo uses the Selenium WebDriver protocol, configured for the Google Chrome web browser, to scrape the National Flood Hazard Layer (NFHL) from the FEMA Map Service Center (MSC).
- **T**: Revelant layers will be selected from the NFHL data and converted to GeoJSON format via QGIS.
- **L**: The GeoJSON file will be uploaded to a Google Cloud Storage bucket to further explore, clean and prepare the data for analysis.


## Run Pipeline

1. Start in your `~/Downloads` directory.
2. `git clone https://github.com/derekz3/NFHL_ETL.git pipeline`
3. `cd pipeline`
4. `chmod +x run.bash`
5. `./run.bash`
6. Enter password when/if prompted.
7. Wait for script to run (~2 minutes).
7. Check `~/Downloads/pipeline/sample` for the `GeoJSON` files.  


## Update '`main`' Branch

1. git add -A
2. git commit -m "[*commit message*]"
3. git push origin main