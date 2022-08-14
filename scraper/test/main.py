from mimetypes import init
import time
from selenium import webdriver
from dotenv import dotenv_values
from user import init_user_data,test_scrape_user_by_id
from post import init_post_links,init_post_data,test_post_data,test_post_link
from comment import test_comment,init_comment

from fastapi import Depends
from sqlalchemy.orm import Session

import sys
import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0].parents[0].parents[0]  # backend root directory
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
from scraper.utils.user_manager import login

DOMAIN = 'https://www.facebook.com'
GROUP_ID = '120212836680964'
GROUP_URL = DOMAIN + '/groups/' + GROUP_ID
SAVECSV = True
SAVEDB = True
LIMIT_ROW = 100
GCP_BUCKET = 'test-image-example-1'


def test():
    
    get_db = init_db.get_session()
    # print("db =",get_db())
    driver = strat_driver()
    
    # init_user_data(init_db.con,get_db)
    
    test_scrape_user_by_id(driver,init_db.con,get_db,DOMAIN,GROUP_URL,'100002537388275',SAVEDB,GCP_BUCKET)
    
    # init_post_links(init_db.con,get_db)
    
    # test_post_link(driver,init_db.con,get_db,DOMAIN,GROUP_URL,SAVECSV,SAVEDB,LIMIT_ROW)
    
    # driver = 0
    # init_post_data(driver,init_db.con,get_db,DOMAIN,GROUP_URL,SAVECSV,SAVEDB,LIMIT_ROW)
    
    # test_post_data(driver,init_db.con,get_db,DOMAIN,GROUP_URL,SAVECSV,SAVEDB,LIMIT_ROW)
    
    # test_comment(driver,init_db.con,get_db,DOMAIN,SAVECSV,SAVEDB,LIMIT_ROW)
    # init_comment(driver,init_db.con,get_db,DOMAIN,GROUP_URL,SAVECSV,SAVEDB,LIMIT_ROW,GCP_BUCKET)
    
def strat_driver():
    #PATH to webdriver
    driver_PATH = os.path.join(FILE.parents[0].parents[0],'chromedriver.exe')
    config = dotenv_values(os.path.join(FILE.parents[0].parents[0],".env"))

    # if mode == 'Init':
    #     SEED_URL = GROUP_URL + '?sorting_setting=CHRONOLOGICAL'
    # else:
    #     SEED_URL = GROUP_URL + '?sorting_setting=RECENT_ACTIVITY' 
        
    COOKIE_PATH = os.path.join(FILE.parents[0].parents[0],'cookies.pkl')

    #disable alert/notifications
    #code by pythonjar
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    #specify the path to chromedriver.exe (download and save on your computer)
    #start the session
    driver = webdriver.Chrome(driver_PATH, chrome_options=chrome_options)
    
    driver.get(DOMAIN)
    
    # Login to facebook
    login(config['USERNAME'],config['PASSWORD'],driver,COOKIE_PATH)
    time.sleep(2)  # Allow 2 seconds for the web success to login

    #We are logged in!

    return driver
    
if __name__ == '__main__':
    test()