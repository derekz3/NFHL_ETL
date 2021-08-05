# NFHL ETL Pipeline  


**DONE** : 'E'—extract and 'T'-transform, Docker  
**NEXT** : Deploy service with Cloud Run


## Summary

- **E**: This repo gathers county-level National Flood Hazard Layer (NFHL) data from the [FEMA Map Service Center](https://msc.fema.gov/portal/advanceSearch#searchresultsanchor) (MSC) by making API requests from the [ArcGIS REST Services Directory](https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer).  
- **T**: Downloaded NFHL data is made available in `shapefile` and GeoJSON-encoded `CSV` formats via [GDAL](https://gdal.org/index.html).  
- **L**: The `CSV` file is first uploaded to a Google Cloud Storage bucket for staging, then transferred to a BigQuery dataset to further explore, clean and prepare the data for analysis.


## Run Pipeline

1. Prerequisites: [Docker](https://docs.docker.com/engine/install/) is installed.
2. Clone repo: `git clone https://github.com/derekz3/NFHL_ETL.git pipeline`
3. Enter repo: `cd pipeline`
4. Run pipeline: `chmod +x run.sh && ./run.sh pipeline [-d DFIRM-ID] [-j INDEX]`
    - `-d, --DFIRM`:  Default is Los Angeles County. Change to any county's FEMA DFIRM-ID.  
    - `-j, --JUMP`:  Default is 0. Jump ahead by `(INDEX * 100)` results for testing purposes.  
    - Example: `chmod +x run.sh && ./run.sh pipeline -d 06111C -j 30`
5. Output files located in `/pipeline/out`. View `/pipeline/out/shape/polygon.shp` in [QGIS](https://qgis.org/en/site/forusers/download.html).
6. Delete Docker image: `docker rmi -f ignite/conda:pipe`  

<br>
