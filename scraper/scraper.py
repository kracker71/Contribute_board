import time
from selenium import webdriver
from dotenv import dotenv_values
from utils.user_manager import login,quit
from utils.post import get_post_info,get_post_link
from utils.user import init_user_collecting

from fastapi import Depends
from sqlalchemy.orm import Session

import sys
import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0].parents[0]  # backend root directory
# print(FILE)
# print(ROOT)

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'backend') not in sys.path:
    sys.path.append(str(ROOT / 'backend'))  # add backend ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# print(os.getcwd())

import logging
from backend.app.database import init_db
from backend.app.crud.post import get_post

# remove duplicated stream handler to avoid duplicated logging
# logging.getLogger().removeHandler(logging.getLogger().handlers[0])

DOMAIN = 'https://www.facebook.com'
GROUP_ID = '120212836680964'
GROUP_URL = DOMAIN + '/groups/' + GROUP_ID
SAVECSV = True
SAVEDB = False
LIMIT_ROW = 100
GCP_BUCKET = 'test-image-example-1'

get_db = init_db.get_db()

def main(mode = 'Update'):
    print('\n',mode,'\n')
    #PATH to webdriver
    driver_PATH = os.path.join(FILE.parents[0],'chromedriver.exe')
    config = dotenv_values(os.path.join(FILE.parents[0],".env"))

    # if mode == 'Init':
    #     SEED_URL = GROUP_URL + '?sorting_setting=CHRONOLOGICAL'
    # else:
    #     SEED_URL = GROUP_URL + '?sorting_setting=RECENT_ACTIVITY' 
        
    COOKIE_PATH = os.path.join(FILE.parents[0],'cookies.pkl')

    #disable alert/notifications
    #code by pythonjar
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    #specify the path to chromedriver.exe (download and save on your computer)
    #start the session
    driver = webdriver.Chrome(driver_PATH, chrome_options=chrome_options)

    #open the webpage
    driver.get(DOMAIN)

    # Login to facebook
    login(config['USERNAME'],config['PASSWORD'],driver,COOKIE_PATH)
    time.sleep(2)  # Allow 2 seconds for the web success to login

    #We are logged in!

    if mode == 'Init':
        ##### GET users info #####
        init_user_collecting(driver,init_db.con,get_db,DOMAIN,GROUP_URL,SAVECSV,SAVEDB,LIMIT_ROW,GCP_BUCKET)
        
        ##### GET post links #####
        _,post_count = get_post_link(driver,init_db.con,Depends(get_db),DOMAIN,GROUP_URL,SAVECSV,SAVEDB,LIMIT_ROW)
        
        # #Query links from DB
        for i in range(0,post_count,LIMIT_ROW):
            post_links = get_post(Depends(get_db),LIMIT_ROW,i)
            # #Get Post INFO
            get_post_info(driver,init_db.con,Depends(get_db),DOMAIN,GROUP_URL,SAVECSV,SAVEDB,LIMIT_ROW,post_links)
        
        
    quit(driver,COOKIE_PATH)
    
if __name__ == '__main__':
    main('Init')