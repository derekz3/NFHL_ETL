# NFHL ETL Pipeline  


**DONE** : 'E'—extract and 'T'-transform so far  
**NEXT** : 'Dockerize' these services + Deploy with Cloud Run


## Summary

- **E**: This repo gathers county-level National Flood Hazard Layer (NFHL) data from the [FEMA Map Service Center](https://msc.fema.gov/portal/advanceSearch#searchresultsanchor) (MSC) via `API requests` from the [ArcGIS REST Services Directory](https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer).  
- **T**: Downloaded NFHL data is made available in `shapefile` and GeoJSON-encoded `CSV` formats via the python library [`GDAL`](https://gdal.org/index.html).  
- **L**: The `CSV` file is first uploaded to a Google Cloud Storage bucket for staging, then transferred to a BigQuery dataset to further explore, clean and prepare the data for analysis.


## Run Pipeline

1. Prerequisites: [`Docker`](https://docs.docker.com/engine/install/)
2. Clone repo: `git clone https://github.com/derekz3/NFHL_ETL.git pipeline`
3. Enter repo: `cd pipeline`
4. Build Docker image: `docker build -t ignite/conda:pipe .`
5. Run Docker image: `docker run -it ignite/conda:pipe /bin/bash`
6. Run script: `python3 fema.py`
7. Get Output file: `sudo docker cp piping:/app/polygon.csv .`
9. Clear: `docker rm $(docker ps -a -q) && docker rmi -f ignite/conda:pipe`


## Update '`main`' Branch

1. git add -A
2. git commit -m "[*commit message*]"
3. git push origin main