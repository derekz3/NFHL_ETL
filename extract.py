import os
import sys
import wget
import time
import subprocess
from time import sleep
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#---------------------------------Setup---------------------------------#


# Require at least Python 3.7
MIN_PYTHON = (3, 7)
assert sys.version_info >= MIN_PYTHON,\
    f"requires Python {'.'.join([str(n) for n in MIN_PYTHON])} or newer"


# [Automate `sudo` with no password]


# Current file location:
# Downloads > pipeline > pipe.py
os.chdir("..")
DOWNLOADS = os.getcwd()


# Check that Chrome is installed
CHROME = os.popen(\
    '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'\
    ).read().split('\n')[0].strip()
if CHROME != 'Google Chrome 92.0.4515.107': # If not, install
    wget.download('https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg')
    os.system('open googlechrome.dmg')
    os.system('sudo cp -r /Volumes/Google\ Chrome/Google\ Chrome.app /Applications/')
    os.system('rm googlechrome.dmg')


# Set up for webdriver download
os.chdir('/usr/local/bin')
BIN = os.getcwd()
bin = os.listdir()


# Download Chrome webdriver executable for M1 MAC if needed
if 'chromedriver' not in bin:
    os.chdir(DOWNLOADS)
    wget.download('https://chromedriver.storage.googleapis.com/92.0.4515.43/chromedriver_mac64_m1.zip')
    with ZipFile('chromedriver_mac64_m1.zip', 'r') as zipObj: 
        zipObj.extractall()
    subprocess.call(['chmod', 'u+x', DOWNLOADS + '/chromedriver'])
    os.system('sudo mv chromedriver ' + BIN)
    os.system('rm chromedriver_mac64_m1.zip')


# Check if webdriver was successfully installed
os.chdir(BIN)
bin = os.listdir()
print(bin)


#--------------------------------Extract--------------------------------#


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

    os.chdir(DOWNLOADS)
    seconds = 0

    for i in range(100):
        proceed, newest = downloading()
        
        if proceed:
            time.sleep(1)
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
        DRIVER = webdriver.Chrome(chrome_options=chrome_options)

    else: DRIVER = webdriver.Chrome()
    PAUSE = pause

    
    # Open FEMA MSC website, which is regularly updated
    DRIVER.get('https://msc.fema.gov/portal/advanceSearch')
    DRIVER.maximize_window()

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
    sleep(10)
    
    complete_download()
    os.chdir(DOWNLOADS)
    with ZipFile('06037C_20210601.zip', 'r') as zipObj: 
        zipObj.extractall('nfhl_layers')
    os.system('rm 06037C_20210601.zip')
    DRIVER.quit()


# Execute main script
extract_lacounty_nfhl(1.5)