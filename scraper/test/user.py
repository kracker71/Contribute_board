import time

from fastapi import HTTPException, Depends
from pydantic import PastDate
from sqlalchemy.orm import Session
from sqlalchemy import String, DateTime, Float,NVARCHAR

from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import pandas as pd
import os
import sys

from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0].parents[0].parents[0]
ROOT_FILE = FILE.parents[0].parents[0]
PAGE = '/members'

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'backend') not in sys.path:
    sys.path.append(str(ROOT / 'backend'))  # add backend ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from scraper.utils.user import scrape_user_data_by_id
# from backend.app.models

def init_user_data(db_conn,db:Session):
    
    csv_user_type = {'user_id' : String(length=100),
                     'user_name' : String(length=100),
                     'user_profile_url' : String(length=2048),'user_profile_picture_url' : String(length=2048),
                     'user_score' : Float,
                     'user_update_score_date' : DateTime
                     }
    
    # user_datetime_col = ['user_update_score_date']
    
    df = pd.read_csv(os.path.join(ROOT_FILE,'result','user','user100.csv'),encoding='utf-8-sig',index_col=False)
    # df = pd.DataFrame(df)
    print(df)
    
    try:
        r = df.to_sql('user',con = db_conn,if_exists='append', index=False,dtype=csv_user_type)
        print(r)
        print("POST SUCCESS")
        # db.commit()
    except :
        print("UNABLE TO POST TO DB")
    ###############################
    
    print("Task Done")
    return df
    # First block is a group user that already collect above
    # tag_name = info_blocks.find_element() 
    
def test_scrape_user_by_id(driver,db_conn,db:Session,domain,group_url,user_id,savedb):
    
    scrape_user_data_by_id(driver,db_conn,db,domain,group_url,user_id,savedb)