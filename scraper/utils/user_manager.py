import time
import pickle
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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

from backend.app.database import init_db


def login(username,password,driver,path):
    
    try:
        # load cookies for given websites
        load_cookie(driver,path)
        driver.refresh()
    except Exception as e:
        # it'll fail for the first time, when cookie file is not present
        print(str(e))
        print("Error loading cookies")
    
    if is_fb_logged_in(driver):
        print("Already logged in")
    else:
        print("Not logged in. Login")
        fb_login(username, password, driver)
        time.sleep(2)
        save_cookie(driver,path)

def is_fb_logged_in(driver):
    # driver.get("https://facebook.com")
    if 'Facebook – log in or sign up' in driver.title:
        return False
    else:
        return True


def fb_login(username, password,driver):
    
    username_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    
    username_box.clear()
    username_box.send_keys(username)
    password_box.clear()
    password_box.send_keys(password)

    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


def save_cookie(driver, cookie_path):
    with open(cookie_path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, cookie_path):
     with open(cookie_path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

def close_all(driver):
    # close all open tabs
    if len(driver.window_handles) < 1:
        return
    for window_handle in driver.window_handles[:]:
        driver.switch_to.window(window_handle)
        driver.close()

def quit(driver,cookie_path):
    save_cookie(driver,cookie_path)
    close_all(driver)
    init_db.con.close()