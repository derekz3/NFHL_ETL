#!/usr/bin/python


import os
import sys
import glob
import geopandas
# from geo import geopandas
from zipfile import ZipFile


gdf = geopandas.read_file('sample/S_FLD_HAZ_AR.shp')
print(gdf.columns.tolist())
print(gdf.shape)
print(gdf.FLD_ZONE.value_counts())


gdf_100yr = gdf.loc[
                (gdf['FLD_ZONE'] == 'AE') |
                (gdf['FLD_ZONE'] == 'AO') | 
                (gdf['FLD_ZONE'] == 'AH') |
                (gdf['FLD_ZONE'] == 'A')
            ]
print(gdf_100yr.shape)
print(gdf_100yr.FLD_ZONE.value_counts())
gdf_100yr.to_file('sample/100yr.geojson', driver='GeoJSON')


gdf_500yr = gdf.loc[
                (gdf['ZONE_SUBTY'] == '0.2 PCT ANNUAL CHANCE FLOOD HAZARD')
            ]
print(gdf_500yr.shape)
print(gdf_500yr.FLD_ZONE.value_counts())
print(gdf_500yr.ZONE_SUBTY.value_counts())
gdf_500yr.to_file('sample/500yr.geojson', driver='GeoJSON')


gdf_urban = gdf.loc[
                (gdf['ZONE_SUBTY'] == '1 PCT DEPTH LESS THAN 1 FOOT')
            ]
print(gdf_urban.shape)
print(gdf_urban.FLD_ZONE.value_counts())
print(gdf_urban.ZONE_SUBTY.value_counts())
gdf_urban.to_file('sample/urban.geojson', driver='GeoJSON')


# Install geopandas using pip
# pip3 install Fiona
# pip3 install Shapely
# pip3 install pyproj
# pip3 install Rtree
# pip3 install geopandas








# os.chdir("../nfhl_layers")
# os.system("find . -depth 1 -type f -not -name '*.shp' -delete")
# os.system("find . -depth 1")