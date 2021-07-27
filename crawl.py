#!/usr/bin/python


import os
import sys
import time
# import geopandas
import subprocess
from time import time
from time import sleep
from pathlib import Path
from zipfile import ZipFile
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Check if element is usable by script
def check_for_element(driver, item, mode, method='ID'):
    
    try:
        
        if mode == 'visible':
            element = WebDriverWait(driver, timeout=20).until(
                EC.visibility_of_element_located((By.ID, item))
            )
        if mode == 'clickable' and method == 'ID':
            element = WebDriverWait(driver, timeout=20).until(
                EC.element_to_be_clickable((By.ID, item))
            )
        if mode == 'clickable' and method == 'CSS':
            element = WebDriverWait(driver, timeout=20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, item))
            )
        if mode == 'clickable' and method == 'XP':
            element = WebDriverWait(driver, timeout=20).until(
                EC.element_to_be_clickable((By.XPATH, item))
            )
        return True
    
    except: return False
    

# Select value from dropdown web element
def select_from_dropdown(driver, pause, item, value):

    # Explicit wait for web element to be visible
    if check_for_element(driver, item, 'visible'):

        # Select and print selection
        dropdown = Select(driver.find_element_by_id(item))
        dropdown.select_by_value(value) # Select
        print(f'Selected {dropdown.first_selected_option.text}!')
    
    sleep(pause)


# Click web element
def click_element(driver, pause, item, method='ID'):

    # Explicit wait for web element to be clickable
    if check_for_element(driver, item, 'clickable') and method == 'ID':
        driver.find_element_by_id(item).click() # Click

    elif check_for_element(driver, item, 'clickable', 'CSS') and method == 'CSS':
        driver.find_element_by_css_selector(item).click() # Click

    elif check_for_element(driver, item, 'clickable', 'XP') and method == 'XP':
        driver.find_element_by_xpath(item).click() # Click
    
    print(f'Clicked on {item}!')
    sleep(pause)


# See if the newest file is still downloading
def downloading():

    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]

    if 'crdownload' in newest or '06037C' not in newest: 
        return True, newest;
    else: 
        return False, newest;


# Quit browser once file is downloaded
def complete_download():

    # HOME = str(Path.home())
    os.chdir('..')
    seconds = 0

    for i in range(60):
        proceed, newest = downloading()
        
        if proceed:
            sleep(1)
            seconds += 1
            print(f'Still Downloading! --- {seconds} seconds --- {newest}')
        
        else: 
            print('Download completed!')
            break


# Click through FEMA MSC to download LA county NFHL data
def extract_lacounty_nfhl(pause, headless=False):


    # Create WebDriver object for Chrome browser
    # Headless mode does not currently work lol
    if headless == True:
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--allow-insecure-localhost");
        chrome_options.add_argument("--disable-gpu");
        chrome_options.add_argument("--no-sandbox");
        user_agent = 'I LIKE CHOCOLATE'
        chrome_options.add_argument(f'user-agent={user_agent}')
        DRIVER = webdriver.Chrome(options=chrome_options)

    else: DRIVER = webdriver.Chrome()
    PAUSE = pause

    
    # Open FEMA MSC website, which is regularly updated
    DRIVER.maximize_window()
    DRIVER.get('https://msc.fema.gov/portal/advanceSearch')

    # Search through 'Jurisdiction' option
    select_from_dropdown(DRIVER, PAUSE, 'selstate', '06')
    select_from_dropdown(DRIVER, PAUSE, 'selcounty', '06037')
    select_from_dropdown(DRIVER, PAUSE, 'selcommunity', '06037C')

    click_element(DRIVER, PAUSE, 'mainSearch')
    click_element(DRIVER, PAUSE, 'eff_root')
    click_element(DRIVER, PAUSE, 'eff_nfhl_county_root')

    download = '#nfhl_county_list > tr:nth-child(1) > td:nth-child(5) > a'
    click_element(DRIVER, PAUSE, download, method='CSS')
    # download = '//*[@id="nfhl_county_list"]/tr[1]/td[5]/a'
    # click_element(DRIVER, PAUSE, download, method='XP')
    
    complete_download()
    os.system('mv 06037C_20210601.zip pipeline')
    os.chdir('pipeline')
    with ZipFile('06037C_20210601.zip', 'r') as zipObj: 
        zipObj.extractall('sample')
    os.system('rm 06037C_20210601.zip')
    os.chdir('sample')
    # Delete all files besides those associated with flood zones ... for now
    os.system("find . -depth 1 -type f -not -name 'S_FLD_HAZ_AR*' -delete")
    DRIVER.quit()


# Execute main script
# extract_lacounty_nfhl(1.5, headless=True)
t0 = time()
extract_lacounty_nfhl(1.5)
t1 = time()
print(f'Extract function takes {t1-t0}')


# Query data prior to geojson:
# gdf = geopandas.read_file('sample/S_FLD_HAZ_AR.shp')
# print(gdf.columns.tolist())
# print(gdf.shape)
# print(gdf.FLD_ZONE.value_counts())


# gdf_100yr = gdf.loc[
#                 (gdf['FLD_ZONE'] == 'AE') |
#                 (gdf['FLD_ZONE'] == 'AO') | 
#                 (gdf['FLD_ZONE'] == 'AH') |
#                 (gdf['FLD_ZONE'] == 'A')
#             ]
# print(gdf_100yr.shape)
# print(gdf_100yr.FLD_ZONE.value_counts())
# gdf_100yr.to_file('sample/100yr.geojson', driver='GeoJSON')


# gdf_500yr = gdf.loc[
#                 (gdf['ZONE_SUBTY'] == '0.2 PCT ANNUAL CHANCE FLOOD HAZARD')
#             ]
# print(gdf_500yr.shape)
# print(gdf_500yr.FLD_ZONE.value_counts())
# print(gdf_500yr.ZONE_SUBTY.value_counts())
# gdf_500yr.to_file('sample/500yr.geojson', driver='GeoJSON')


# gdf_urban = gdf.loc[
#                 (gdf['ZONE_SUBTY'] == '1 PCT DEPTH LESS THAN 1 FOOT')
#             ]
# print(gdf_urban.shape)
# print(gdf_urban.FLD_ZONE.value_counts())
# print(gdf_urban.ZONE_SUBTY.value_counts())
# gdf_urban.to_file('sample/urban.geojson', driver='GeoJSON')